from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_db_connection
from psycopg2.extras import RealDictCursor

class Item(BaseModel):
    id_author: int
    name_author: str
    address: str
    email_author: str


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/authors")
async def get_authors():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM "Libreria".authors;')
        authors = cur.fetchall()
        cur.close()
        conn.close()
        return authors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))