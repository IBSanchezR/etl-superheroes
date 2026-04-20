import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

mode = os.getenv("DB_MODE", "local")

# =========================
# CONEXIÓN DINÁMICA
# =========================
if mode == "local":
    conn = psycopg2.connect(
        dbname=os.getenv("LOCAL_DB_NAME"),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        host=os.getenv("LOCAL_DB_HOST"),
        port=os.getenv("LOCAL_DB_PORT")
    )
else:
    conn = psycopg2.connect(
        dbname=os.getenv("SUPA_DB_NAME"),
        user=os.getenv("SUPA_DB_USER"),
        password=os.getenv("SUPA_DB_PASSWORD"),
        host=os.getenv("SUPA_DB_HOST"),
        port=os.getenv("SUPA_DB_PORT"),
        sslmode="require"
    )

cur = conn.cursor()

print(f"=== CONSULTAS SUPERHÉROES ({mode.upper()}) ===\n")

# =========================
# 1. Total de héroes
# =========================
cur.execute("SELECT COUNT(*) FROM heroes;")
total = cur.fetchone()[0]
print(f"Total de héroes: {total}\n")

# =========================
# 2. Top 5 más fuertes
# =========================
cur.execute("""
    SELECT name, strength
    FROM heroes
    WHERE strength IS NOT NULL
    ORDER BY strength DESC
    LIMIT 5;
""")

print("Top 5 más fuertes:")
for row in cur.fetchall():
    print(row)
print()

# =========================
# 3. Promedio de poder
# =========================
cur.execute("""
    SELECT AVG(power)
    FROM heroes
    WHERE power IS NOT NULL;
""")

avg_power = cur.fetchone()[0]
print(f"Promedio de poder: {avg_power:.2f}\n")

# =========================
# 4. Conteo por publisher
# =========================
cur.execute("""
    SELECT publisher, COUNT(*)
    FROM heroes
    GROUP BY publisher
    ORDER BY COUNT(*) DESC
    LIMIT 5;
""")

print("Top publishers:")
for row in cur.fetchall():
    print(row)
print()

# =========================
# 5. Alineación
# =========================
cur.execute("""
    SELECT alignment, COUNT(*)
    FROM heroes
    GROUP BY alignment;
""")

print("Distribución de alineación:")
for row in cur.fetchall():
    print(row)
print()

# =========================
# 6. Estadísticas de poder por publisher
# =========================
cur.execute("""
    SELECT 
        publisher,
        ROUND(AVG(power)::numeric, 1) AS promedio,
        MIN(power) AS minimo,
        MAX(power) AS maximo
    FROM heroes
    WHERE power IS NOT NULL
    GROUP BY publisher
    ORDER BY AVG(power) DESC;
""")

print("Estadísticas de poder por publisher:")
for row in cur.fetchall():
    print(row)
print()

# =========================
# CIERRE
# =========================
cur.close()
conn.close()

print("Consultas ejecutadas correctamente ✅")