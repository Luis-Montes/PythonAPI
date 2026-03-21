from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_db_connection
from psycopg2.extras import RealDictCursor

# Inserts para autores
class ItemAuthor(BaseModel):
    name_author: str
    lastname_author: str
    address: str
    email_author: str

# Inserts para libros
class ItemBook(BaseModel):
    name_book: str
    description_book: str
    price_book: float
    id_author: int
    stocks: int


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Rutas para autores

@app.get("/authors")
def get_authors():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT name_author, lastname_author, address, email_author FROM "Libreria".authors;')
        authors = cur.fetchall()
        cur.close()
        conn.close()
        return authors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/authors/{id_author}")
def get_author(id_author: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM "Libreria".authors WHERE id_author = %s', (id_author,))
        author = cur.fetchone()
        cur.close()
        conn.close()
        if author:
            return author
        else:
            raise HTTPException(status_code=404, detail="Error al encontrar el autor")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el autor: {e}")

@app.post("/authors")
def create_author(ItemAuthor: ItemAuthor):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('INSERT INTO "Libreria".authors (name_author, lastname_author, address, email_author) VALUES (%s, %s, %s, %s) RETURNING id_author;',
                    (ItemAuthor.name_author, ItemAuthor.lastname_author, ItemAuthor.address, ItemAuthor.email_author))
        new_id = cur.fetchone()['id_author']
        print(f"Nuevo autor creado con ID: {new_id}")
        cur.close()
        conn.commit()
        conn.close()
        return {"id_author": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rutas para libros

@app.get("/books")
def books():
    try:
        conn = get_db_connection()
        cur = conn .cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT 
            name_book, 
            description_book, 
            price_book, 
            name_author || ' ' || lastname_author AS full_name,
            stocks
        FROM "Libreria".books 
        LEFT JOIN "Libreria".authors ON "Libreria".books.id_author = "Libreria".authors.id_author;
"""
        cur.execute(query)
        books = cur.fetchall()
        cur.close()
        conn.close()
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/books")
def create_book(ItemBook: ItemBook):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('INSERT INTO "Libreria".books (name_book, description_book, price_book, id_author, stocks) VALUES (%s, %s, %s, %s, %s) RETURNING id_book;',
                    (ItemBook.name_book, ItemBook.description_book, ItemBook.price_book, ItemBook.id_author, ItemBook.stocks))
        new_id = cur.fetchone()['id_book']
        print(f"Nuevo libro creado con ID: {new_id}")
        cur.close()
        conn.commit()
        conn.close()
        return {"id_book": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.put("/books/{id_book}")
# def update_book(id_book: int, ItemBook: ItemBook):
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor(cursor_factory=RealDictCursor)

#         cur.execute(
#             'UPDATE "Libreria".books SET price_book = %s, stocks = %s WHERE id_book = %s RETURNING id_book;',
#             (ItemBook.price_book, ItemBook.stocks, id_book)
#         )

#         result = cur.fetchone()
#         if not result:
#             raise HTTPException(status_code=404, detail="Libro no encontrado")

#         conn.commit()
#         return {"id_book": result['id_book']}

#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         cur.close()
#         conn.close()