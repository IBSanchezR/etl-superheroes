import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# =========================
# CONFIGURACIÓN
# =========================
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

# =========================
# CARGA DE DATOS
# =========================
query = "SELECT * FROM heroes;"
df = pd.read_sql(query, conn)

# =========================
# INTERFAZ
# =========================
st.title("🦸‍♂️ Dashboard de Análisis de Superhéroes")
st.markdown("Análisis exploratorio de habilidades y afiliaciones de personajes de cómics")

st.metric("Total de héroes", df.shape[0])

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

publisher = st.sidebar.selectbox(
    "Selecciona un publisher",
    ["Todos"] + list(df["publisher"].dropna().unique())
)

search = st.sidebar.text_input("Buscar héroe")

# Aplicar filtros
if publisher != "Todos":
    df = df[df["publisher"] == publisher]

if search:
    df = df[df["name"].str.contains(search, case=False, na=False)]

# =========================
# TABLA
# =========================
st.subheader("Datos de héroes")
st.dataframe(df.head(50))

# =========================
# TOP 10 FUERZA
# =========================
st.subheader("Top 10 más fuertes")

top_strength = df.dropna(subset=["strength"]).sort_values(by="strength", ascending=False).head(10)
st.bar_chart(top_strength.set_index("name")["strength"])

# =========================
# DISTRIBUCIÓN ALIGNMENT
# =========================
st.subheader("Distribución de alineación")

alignment_counts = df["alignment"].value_counts()
st.bar_chart(alignment_counts)

# =========================
# DISTRIBUCIÓN PUBLISHER
# =========================
st.subheader("Distribución por publisher")

publisher_counts = df["publisher"].value_counts().head(10)
st.bar_chart(publisher_counts)

# =========================
# PROMEDIO DE PODER
# =========================
st.subheader("Promedio de poder por publisher")

power_avg = (
    df.dropna(subset=["power"])
    .groupby("publisher")["power"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(power_avg)

# =========================
# MIN Y MAX DE PODER
# =========================
st.subheader("Mínimo y máximo de poder por publisher")

power_stats = (
    df.dropna(subset=["power"])
    .groupby("publisher")["power"]
    .agg(["mean", "min", "max"])
    .sort_values(by="mean", ascending=False)
    .head(10)
)

st.dataframe(power_stats)

# =========================
# RANKING GENERAL
# =========================
st.subheader("Ranking general de poder")

top_power = df.dropna(subset=["power"]).sort_values(by="power", ascending=False).head(10)
st.dataframe(top_power[["name", "power", "publisher"]])

# =========================
# CIERRE CONEXIÓN
# =========================
conn.close()