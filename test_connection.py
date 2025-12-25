from ecotech import Database

db = Database()

try:
    with db.connect() as conn:
        print("Conexion OK")
except Exception as e:
    print("Error:", e)
