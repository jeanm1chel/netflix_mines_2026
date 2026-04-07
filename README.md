# 🎬 CinéAPI — Backend façon Netflix

Bienvenue dans ce projet fil rouge ! Tu vas construire de A à Z un backend de streaming de films, inspiré de Netflix, en utilisant **FastAPI** et **SQLite**.

---

## 🗺️ Vue d'ensemble

| Séance | Thème | Objectifs |
|--------|-------|-----------|
| 1 | Fondations | Premiers endpoints, design de la base de données |
| 2 | Fonctionnalités | Visualisation, comptes utilisateurs |
| 3 | Cybersécurité | Sécurisation de l'API + évaluation orale |

---

## 🛠️ Stack technique

- **Python 3.11+**
- **FastAPI** — framework web moderne et rapide
- **SQLite** — base de données légère, fichier local
- **Raw SQL** avec le module `sqlite3` de Python

---

## ⚙️ Installation

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd cineapi

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
fastapi dev main.py
```

L'API est accessible sur `http://localhost:8000`  
La documentation interactive est disponible sur `http://localhost:8000/docs`

---

## 📅 Séance 1 — Fondations : endpoints & base de données

### Objectifs
- Comprendre la structure d'un projet FastAPI
- Concevoir le schéma de la base de données ensemble
- Implémenter les premiers endpoints CRUD

### Routes à implémenter

#### Films

**`GET /films`** — Lister les films (avec pagination)

| Paramètre | Type | Requis | Défaut | Description |
|-----------|------|--------|--------|-------------|
| `page` | query (int) | non | `1` | Numéro de page |
| `per_page` | query (int) | non | `20` | Nombre de films par page |
| `genre_id` | query (int) | non | — | Filtrer par genre |

Réponse `200` — `PaginatedResponse` :
```json
{
  "data": [FilmResponse],
  "page": 1,
  "per_page": 20,
  "total": 100
}
```

---

**`GET /films/{film_id}`** — Détail d'un film

| Paramètre | Type | Requis |
|-----------|------|--------|
| `film_id` | path (int) | oui |

Réponse `200` — `FilmResponse` :
```json
{
  "ID": 1,
  "Nom": "Inception",
  "Note": 8.8,
  "DateSortie": 2010,
  "Image": "https://...",
  "Video": "https://...",
  "Genre_ID": 3
}
```

> Les champs `Note`, `DateSortie`, `Image`, `Video` et `Genre_ID` sont optionnels (peuvent être `null`). Seuls `ID` et `Nom` sont obligatoires.

#### Genres

**`GET /genres`** — Lister tous les genres

Aucun paramètre.

Réponse `200` — liste de `GenreResponse` :
```json
[
  { "ID": 1, "Type": "Action" },
  { "ID": 2, "Type": "Comédie" }
]
```

### Notions abordées
- Structure d'un projet FastAPI (`main.py`, routeurs, schémas Pydantic)
- Méthodes HTTP et codes de statut (200, 201, 404…)
- Modélisation relationnelle (clés primaires, clés étrangères)

---

## 📅 Séance 2 — Auth & préférences utilisateur

### Objectifs
- Gérer les utilisateurs et l'authentification par token JWT
- Implémenter un système de préférences par genre
- Recommander des films en fonction des préférences

### Routes à implémenter

#### Auth

**`POST /auth/register`** — Créer un compte

Body JSON :
```json
{
  "email": "user@example.com",
  "pseudo": "johndoe",
  "password": "s3cret"
}
```

Réponse `200` — `TokenResponse` :
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

---

**`POST /auth/login`** — Se connecter

Body JSON :
```json
{
  "email": "user@example.com",
  "password": "s3cret"
}
```

Réponse `200` — `TokenResponse` :
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

#### Preferences

> Toutes les routes `/preferences` nécessitent le header `Authorization: Bearer <token>`.

**`POST /preferences`** — Ajouter un genre en favori

| Paramètre | Type | Requis |
|-----------|------|--------|
| `Authorization` | header (string) | oui |

Body JSON :
```json
{
  "genre_id": 3
}
```

Réponse `201`.

---

**`DELETE /preferences/{genre_id}`** — Retirer un genre des favoris

| Paramètre | Type | Requis |
|-----------|------|--------|
| `genre_id` | path (int) | oui |
| `Authorization` | header (string) | oui |

Réponse `200`.

---

**`GET /preferences/recommendations`** — Films recommandés selon les préférences

| Paramètre | Type | Requis |
|-----------|------|--------|
| `Authorization` | header (string) | oui |

Réponse `200` — liste de `FilmResponse` :
```json
[
  { "ID": 1, "Nom": "Inception", "Note": 8.8, "Genre_ID": 3 }
]
```

### Notions abordées
- Authentification par token JWT
- Hashage des mots de passe (`bcrypt`)
- Utilisation du module `sqlite3` : `cursor`, `fetchall`, `fetchone`
- Requêtes avec jointures

---

## 📅 Séance 3 — Cybersécurité & évaluation

### Objectifs
- Comprendre les principales vulnérabilités d'une API REST
- Présenter et défendre son travail à l'oral

### Ce qu'on construit
- Middleware de rate limiting sur les endpoints sensibles
- Retour d'erreurs `429 Too Many Requests`
- Stratégies de limitation : par IP, par utilisateur

### Notions abordées
- Rate limiting : pourquoi et comment (attaques par force brute, DDoS applicatif)
- Implémentation maison : compteur de requêtes en mémoire (`dict`, timestamps)

### 🎤 Évaluation orale
Chaque étudiant présente **son code** et des questions seront posées

---

## 📖 Référence des modèles

| Modèle | Champs | Requis |
|--------|--------|--------|
| `FilmResponse` | `ID` (int), `Nom` (string), `Note` (float?), `DateSortie` (int?), `Image` (string?), `Video` (string?), `Genre_ID` (int?) | `ID`, `Nom` |
| `GenreResponse` | `ID` (int), `Type` (string) | tous |
| `PaginatedResponse` | `data` (array), `page` (int), `per_page` (int), `total` (int) | tous |
| `TokenResponse` | `access_token` (string), `token_type` (string, défaut: `"bearer"`) | `access_token` |

### Utilitaire

**`GET /ping`** — Health check

Réponse `200`.

## 📚 Ressources utiles

- [Documentation FastAPI](https://fastapi.tiangolo.com)
- [SQLite Browser](https://sqlitebrowser.org) — visualiser ta BDD

---

*Bon courage ! 🚀*
