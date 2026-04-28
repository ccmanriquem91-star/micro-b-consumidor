import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Railway configura DATABASE_URL automáticamente si está vinculada
DATABASE_URL = os.getenv("DATABASE_URL")

class Data(BaseModel):
    user: str

@app.get("/")
def health_check():
    return {"status": "Micro B vivo y esperando datos"}

@app.post("/procesar")
def procesar_dato(item: Data):
    conn = None
    try:
        # Conexión con SSL requerido para Railway
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        # Insertar el dato en la tabla
        query = "INSERT INTO registros (nombre) VALUES (%s)"
        cur.execute(query, (item.user,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "message": f"Usuario {item.user} guardado en Postgres"}
    
    except Exception as e:
        if conn:
            conn.close()
        return {"status": "error", "message": str(e)}
