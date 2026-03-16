import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables desde el archivo .env (ruta relativa a este archivo)
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

@app.get("/authors/{id_author}")
def get_author(id_author: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM authors WHERE id = %s", (id_author,))
        author = cur.fetchone()
        cur.close()
        conn.close()
        if author:
            return author
        else:
            raise HTTPException(status_code=404, detail="Error al encontrar el autor")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el autor: {e}")