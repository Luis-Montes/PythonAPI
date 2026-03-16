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
def get_authors():
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

@app.post("/authors")
def create_author(item: Item):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('INSERT INTO "Libreria".authors (id, name, address, email) VALUES (%s, %s, %s, %s) RETURNING id;',
                    (item.id_author, item.name_author, item.address, item.email_author))
        new_id = cur.fetchone()['id']
        cur.close()
        conn.commit()
        conn.close()
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))