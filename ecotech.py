import oracledb
import bcrypt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.user = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASSWORD")
        self.dsn = os.getenv("ORACLE_DSN")

    def connect(self):
        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn
        )

    def execute(self, sql, params=None, fetch=False):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or {})
                if fetch:
                    return cur.fetchall()
            conn.commit()

class Auth:
    @staticmethod
    def register(db, user_id, name, password):
        name = name.strip().upper()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).hex()

        db.execute(
            "INSERT INTO USERS (ID, NAME, PASSWORD) VALUES (:id, :n, :p)",
            {"id": user_id, "n": name, "p": hashed}
        )

    @staticmethod
    def login(db, name, password):
        name = name.strip().upper()
        r = db.execute(
            "SELECT PASSWORD FROM USERS WHERE NAME = :n",
            {"n": name},
            fetch=True
        )
        if not r:
            return False
        return bcrypt.checkpw(password.encode(), bytes.fromhex(r[0][0]))

class Finance:
    BASE = "https://mindicador.cl/api"

    @staticmethod
    def get(indicator):
        r = requests.get(f"{Finance.BASE}/{indicator}", timeout=10)
        data = r.json()
        return data["serie"][0]["valor"], data["serie"][0]["fecha"]

class Consultas:
    @staticmethod
    def guardar(db, name, indicator, fecha, valor):
        db.execute(
            """
            INSERT INTO CONSULTAS (NAME, INDICATOR, DATE_QUERY, VALUE, SOURCE)
            VALUES (:n, :i, TO_DATE(:d, 'YYYY-MM-DD'), :v, 'mindicador.cl')
            """,
            {
                "n": name,
                "i": indicator,
                "d": fecha[:10],
                "v": float(valor)
            }
        )

    @staticmethod
    def historial(db, name):
        return db.execute(
            """
            SELECT INDICATOR,
                   TO_CHAR(DATE_QUERY,'YYYY-MM-DD'),
                   VALUE
            FROM CONSULTAS
            WHERE NAME = :n
            ORDER BY CREATED_AT DESC
            """,
            {"n": name},
            fetch=True
        )
