import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    # =========================
    # INTENTO 1: STREAMLIT CLOUD
    # =========================
    try:
        import streamlit as st

        host = st.secrets.get("DB_HOST", "")

        # IMPORTANTE: evitar localhost en nube
        if host and host != "localhost":
            return {
                "host": host,
                "port": st.secrets.get("DB_PORT", "5432"),
                "user": st.secrets.get("DB_USER", "postgres"),
                "password": st.secrets.get("DB_PASSWORD", ""),
                "dbname": st.secrets.get("DB_NAME", "postgres"),
                "sslmode": st.secrets.get("DB_SSLMODE", "require"),
            }

    except Exception:
        pass  # no está en Streamlit Cloud

    # =========================
    # INTENTO 2: LOCAL (.env)
    # =========================
    mode = os.getenv("DB_MODE", "local")

    if mode == "local":
        return {
            "host": os.getenv("LOCAL_DB_HOST", "localhost"),
            "port": os.getenv("LOCAL_DB_PORT", "5432"),
            "user": os.getenv("LOCAL_DB_USER", "postgres"),
            "password": os.getenv("LOCAL_DB_PASSWORD", ""),
            "dbname": os.getenv("LOCAL_DB_NAME", "superheroes"),
        }
    else:
        return {
            "host": os.getenv("SUPA_DB_HOST"),
            "port": os.getenv("SUPA_DB_PORT", "6543"),
            "user": os.getenv("SUPA_DB_USER"),
            "password": os.getenv("SUPA_DB_PASSWORD"),
            "dbname": os.getenv("SUPA_DB_NAME", "postgres"),
            "sslmode": os.getenv("SUPA_DB_SSLMODE", "require"),
        }
