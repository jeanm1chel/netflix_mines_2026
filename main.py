from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection
import jwt

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

class Film(BaseModel):
    id: int | None = None
    nom: str
    note: float | None = None
    dateSortie: int
    image: str | None = None
    video: str | None = None
    genreId: int | None = None

class PaginatedResponse(BaseModel):
    data : list 
    page : int | None = 1
    per_page : int | None = 20
    total : int 

class User(BaseModel):
    email : str | None = None
    pseudo : str 
    password : str 
    disabled : bool | None = None

class TokenResponse(BaseModel):
    access_token : str
    token_type : str | None = "bearer"


@app.post("/film")
async def createFilm(film : Film):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO Film (Nom,Note,DateSortie,Image,Video)  
            VALUES('{film.nom}',{film.note},{film.dateSortie},'{film.image}','{film.video}') RETURNING *
            """)
        res = cursor.fetchone()
        print(res)
        return res

@app.get("/film")
async def getFilms(page = 1, per_page = 20, genre_id = None):
    per_page=int(per_page)
    page=int(page)
    with get_connection() as conn:
        cursor = conn.cursor()
        if genre_id == None:
            cursor.execute(f"SELECT * FROM Film ORDER BY Genre_ID,DateSortie  LIMIT {per_page} OFFSET {(page-1)*per_page}")
        else:
            cursor.execute(f"SELECT * FROM Film WHERE Genre_ID = {genre_id} ORDER BY DateSortie LIMIT {per_page} OFFSET {(page-1)*per_page}")
        data = cursor.fetchall()
        cursor = conn.cursor()
        if genre_id == None:
            cursor.execute(f"SELECT COUNT(*) FROM Film")
        else:
            cursor.execute(f"SELECT COUNT(*) FROM Film WHERE Genre_ID = {genre_id}")
        res = {"data" : data, "page": page, "per_page":per_page, "total": cursor.fetchone()}
        return res



@app.get("/genres")
async def getGenres():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Genre")
        res = cursor.fetchall()  
        return res
    
@app.get("/film/{id}")
async def getFilm(id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Film WHERE Id = {id}")
        res = cursor.fetchone()
        return res

@app.delete("/film/{id}")
async def deleteFilm(id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM Film WHERE Id = {id}")
        return {"message": f"Film {id} supprimé"}
    
# Authentification

@app.post("/auth/register")
async def createAccount(user: User):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
        f"""
            INSERT INTO Utilisateur (AdresseMail,Pseudo,MotDePasse)  
            VALUES('{user.email}','{user.pseudo}','{user.password}') RETURNING *
            """)
        res = cursor.fetchone()
        print(res)
        token = jwt.encode({"code": user.email,}, SECRET_KEY, algorithm="HS256")

    return TokenResponse(access_token=token, token_type="bearer")


@app.post("/auth/login")
async def login(user: User):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM Utilisateur WHERE AdresseMail = '{user.email}' AND MotDePasse = '{user.password}'"
        )
        res = cursor.fetchone()

    if res is None:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    token = jwt.encode({"sub": user.email}, SECRET_KEY,algorithm="HS256")

    return TokenResponse(access_token=token, token_type="bearer")

@app.post("preferences")
async def addPref():
    return 

@app.delete("preferences/{genre_id}")
async def delPref(genre_id, Authorization):
    return 
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
