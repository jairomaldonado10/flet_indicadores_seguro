import os
import bcrypt
import oracledb
import requests
import datetime
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
    def register(db, user_id, username, password):
        if not username or not password:
            raise ValueError("Campos vacíos")

        if len(password) < 6:
            raise ValueError("Contraseña mínima 6 caracteres")

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).hex()

        db.execute(
            "INSERT INTO USERS (ID, NAME, PASSWORD) VALUES (:id, :name, :pass)",
            {"id": user_id, "name": username, "pass": hashed}
        )

    @staticmethod
    def login(db, username, password):
        rows = db.execute(
            "SELECT PASSWORD FROM USERS WHERE NAME = :name",
            {"name": username},
            fetch=True
        )

        if not rows:
            return False

        stored = bytes.fromhex(rows[0][0])
        return bcrypt.checkpw(password.encode(), stored)

class Finance:
    @staticmethod
    def get(indicator, date=None):
        url = f"https://mindicador.cl/api/{indicator}"
        if date:
            date = date.replace("-", "")
            url += f"/{date}"

        r = requests.get(url, timeout=10)
        data = r.json()

        serie = data["serie"][0]
        return serie["valor"], serie["fecha"]

class Consultas:
    @staticmethod
    def save(db, user, indicator, value):
        db.execute(
            """
            INSERT INTO CONSULTAS
            (NAME, INDICATOR, VALUE, SOURCE, DATE_QUERY)
            VALUES (:n, :i, :v, 'mindicador.cl', SYSDATE)
            """,
            {"n": user, "i": indicator, "v": value}
        )

    @staticmethod
    def history(db, user):
        return db.execute(
            """
            SELECT INDICATOR, VALUE, DATE_QUERY
            FROM CONSULTAS
            WHERE NAME = :n
            ORDER BY DATE_QUERY DESC
            """,
            {"n": user},
            fetch=True
        )
