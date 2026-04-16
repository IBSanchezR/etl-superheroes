import streamlit as st
import pandas as pd
import psycopg2

# =========================
# CONEXIÓN A POSTGRESQL
# =========================
conn = psycopg2.connect(
    dbname="superheroes",
    user="postgres",
    password="SuperHero2026!",
    host="localhost",
    port="5432"
)

query = "SELECT * FROM heroes;"
df = pd.read_sql(query, conn)

# =========================
# INTERFAZ
# =========================
st.title("🦸‍♂️ Dashboard de Análisis de Superhéroes")
st.markdown("Análisis exploratorio de habilidades y afiliaciones de personajes de cómics")

st.write(f"Total de héroes: {df.shape[0]}")

# =========================
# FILTRO POR PUBLISHER
# =========================
st.sidebar.header("Filtros")

publisher = st.sidebar.selectbox(
    "Selecciona un publisher",
    ["Todos"] + list(df["publisher"].dropna().unique())
)

if publisher != "Todos":
    df = df[df["publisher"] == publisher]

# =========================
# TABLA
# =========================
st.subheader("Datos de héroes")
st.dataframe(df.head(50))

# =========================
# TOP 10 FUERZA
# =========================
st.subheader("Top 10 más fuertes")

top_strength = df.sort_values(by="strength", ascending=False).head(10)
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

#===========================
#PROMEDIO DE PODER POR PUBLISHER
#===========================

st.subheader("Promedio de poder por publisher")

power_avg = df.groupby("publisher")["power"].mean().sort_values(ascending=False).head(10)
st.bar_chart(power_avg)

# =========================
# BÚSQUEDA DE HÉROES
# =========================
search = st.sidebar.text_input("Buscar héroe")

if search:
    df = df[df["name"].str.contains(search, case=False, na=False)]
    st.subheader(f"Héroes que coinciden con '{search}'")
    
# =========================
# RANKING GENERAL DE PODER
# =========================

st.subheader("Ranking general de poder")
top_power = df.sort_values(by="power", ascending=False).head(10)
st.dataframe(top_power[["name", "power", "publisher"]])

