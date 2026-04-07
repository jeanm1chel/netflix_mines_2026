from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

class Film(BaseModel):
    id: int | None = None
    nom: str
    note: float | None = None
    dateSortie: int
    image: str | None = None
    video: str | None = None
    genreId: int | None = None

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
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Film ORDER BY {genre_id} LIMIT {per_page} OFFSET {(page-1)*per_page}")
        res = cursor.fetchall()  
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
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
