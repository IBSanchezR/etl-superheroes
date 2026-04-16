import os
import json
import logging
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv


# =========================
# CONFIGURACIÓN
# =========================
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

DATA_DIR = Path("data")
LOG_DIR = Path("logs")

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# EXTRACCIÓN
# =========================
def fetch_hero(hero_id):
    url = f"{BASE_URL}/{API_KEY}/{hero_id}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            if data.get("response") == "success":
                logging.info(f"Heroe {hero_id} extraído correctamente")
                return data
            else:
                logging.warning(f"Heroe {hero_id} no válido")
        else:
            logging.error(f"Error HTTP {response.status_code} en ID {hero_id}")

    except Exception as e:
        logging.error(f"Error en ID {hero_id}: {e}")

    return None


# =========================
# LIMPIEZA
# =========================
def clean_value(value):
    if value in ["-", "null", "", None, "None"]:
        return None
    return value


def clean_int(value):
    value = clean_value(value)
    if value is None:
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


# =========================
# TRANSFORMACIÓN
# =========================
def transform_hero(data):
    return {
        "id": clean_int(data.get("id")),
        "name": clean_value(data.get("name")),
        "intelligence": clean_int(data["powerstats"].get("intelligence")),
        "strength": clean_int(data["powerstats"].get("strength")),
        "speed": clean_int(data["powerstats"].get("speed")),
        "durability": clean_int(data["powerstats"].get("durability")),
        "power": clean_int(data["powerstats"].get("power")),
        "combat": clean_int(data["powerstats"].get("combat")),
        "publisher": clean_value(data["biography"].get("publisher")),
        "alignment": clean_value(data["biography"].get("alignment")),
        "gender": clean_value(data["appearance"].get("gender")),
        "race": clean_value(data["appearance"].get("race")),
    }


# =========================
# PROCESO PRINCIPAL
# =========================
def main():
    heroes_raw = []
    heroes_clean = []

    print("Iniciando extracción...")

    for hero_id in range(1, 732):
        print(f"Procesando héroe {hero_id}...")
        data = fetch_hero(hero_id)

        if data:
            heroes_raw.append(data)
            heroes_clean.append(transform_hero(data))

    with open(DATA_DIR / "heroes_raw.json", "w", encoding="utf-8") as f:
        json.dump(heroes_raw, f, indent=4, ensure_ascii=False)

    df = pd.DataFrame(heroes_clean)

    cols_int = ["id", "intelligence", "strength", "speed", "durability", "power", "combat"]
    for col in cols_int:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df.to_csv(DATA_DIR / "heroes.csv", index=False)

    print("ETL completado ✅")
    print(f"JSON: {DATA_DIR / 'heroes_raw.json'}")
    print(f"CSV: {DATA_DIR / 'heroes.csv'}")


if __name__ == "__main__":
    main()