import os
import pymysql

def query(sql, params=(), one=False):
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rmlk"),
        database=os.getenv("DB_NAME", "viajero_frecuente"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if sql.lstrip().upper().startswith("SELECT"):
                return cur.fetchone() if one else cur.fetchall()
            return cur.lastrowid
    finally:
        conn.close()
