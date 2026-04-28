import os
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2 # Librería para PostgreSQL

app = FastAPI()

# Railway te dará esta variable automáticamente al conectar la DB
DATABASE_URL = os.getenv("DATABASE_URL")

class Data(BaseModel):
    user: str

@app.post("/procesar")
def procesar_dato(item: Data):
    # Lógica para guardar en la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO registros (nombre) VALUES (%s)", (item.user,))
    conn.commit()
    cur.close()
    conn.close()
    
    return {"message": f"Usuario {item.user} guardado en la base de datos gestionada"}
