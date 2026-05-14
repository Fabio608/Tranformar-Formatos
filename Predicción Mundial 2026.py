import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Mundial 2026 - Predicción vs Realidad", page_icon="🏆", layout="wide")

# Lógica de Tiempo (Local Argentina UTC-3)
AR = timezone(timedelta(hours=-3))
fecha_apertura_reales = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
ahora = datetime.now(AR)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;700;900&display=swap');

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background-color: #FFFFFF !important; 
        border-radius: 20px;
        padding: 30px 50px;
    }
    
    .titulo-principal {
        font-family: 'Archivo Black', sans-serif;
        color: #1a472a;
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 20px;
    }

    .titulo-zona {
        font-family: 'Archivo Black', sans-serif;
        color: #FF8C00 !important; /* Anaranjado brillante */
        font-size: 1.8rem !important;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 3px solid #FF8C00;
        width: fit-content;
    }

    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }

    .titulo-posiciones {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    div[data-testid="stNumberInput"] { width: 55px !important; }
    input { font-weight: 800 !important; color: #1a472a !important; }

    [data-testid="stTable"] {
        background-color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: black !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)

# --- 2. TODOS LOS GRUPOS (A - L) ---
mundial = {
        "ZONA A": ["México", "Sudáfrica", "Corea del Sur", "República Checa"],
        "ZONA B": ["Canadá", "Bosnia", "Qatar", "Suiza"],
        "ZONA C": ["Brasil", "Marruecos", "Haití", "Escocia"],
        "ZONA D": ["Estados Unidos", "Australia", "Paraguay", "Turquía"],
        "ZONA E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
        "ZONA F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
        "ZONA G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
        "ZONA H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
        "ZONA I": ["Francia", "Senegal", "Irak", "Noruega"],
        "ZONA J": ["Argentina", "Argelia", "Jordania", "Austria"],
        "ZONA K": ["Portugal", "RD Congo", "Uzbekistán", "Colombia"],
        "ZONA L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
    }

# Función para MI PREDICCIÓN (Nombres completos de columnas)
def calcular_df_estricto(equipos, resultados_dict):
    tabla = pd.DataFrame({
        'Equipo': equipos, 
        'Puntos': 0, 
        'Partidos Jugados': 0, 
        'Goles a Favor': 0, 
        'Goles en Contra': 0, 
        'Diferencia de Goles': 0
    }).set_index('Equipo')
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            if g1 > 0 or g2 > 0 or (g1 == 0 and g2 == 0 and f"p_{e1}_{e2}" in st.session_state):
                tabla.loc[e1, 'Partidos Jugados'] += 1
                tabla.loc[e2, 'Partidos Jugados'] += 1
                tabla.loc[e1, 'Goles a Favor'] += g1
                tabla.loc[e1, 'Goles en Contra'] += g2
                tabla.loc[e2, 'Goles a Favor'] += g2
                tabla.loc[e2, 'Goles en Contra'] += g1
                if g1 > g2: tabla.loc[e1, 'Puntos'] += 3
                elif g2 > g1: tabla.loc[e2, 'Puntos'] += 3
                else:
                    tabla.loc[e1, 'Puntos'] += 1
                    tabla.loc[e2, 'Puntos'] += 1
    tabla['Diferencia de Goles'] = tabla['Goles a Favor'] - tabla['Goles en Contra']
    return tabla.sort_values(by=['Puntos', 'Diferencia de Goles', 'Goles a Favor'], ascending=False)

# --- 3. INTERFAZ ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

# SOLAPA 1: MI PREDICCIÓN
with tab_p:
    nombre = st.text_input("👤 **TU NOMBRE:**")
    user_input_now = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c_partidos, c_tabla = st.columns([1, 1.4]) # Ajuste de ancho para nombres largos
        with c_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with cols[0]: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    g1 = cols[1].number_input("", 0, 20, 0, key=f"p_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    with cols[2]: st.markdown("<p style='text-align:center; font-weight:900;'>-</p>", unsafe_allow_html=True)
                    g2 = cols[3].number_input("", 0, 20, 0, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    with cols[4]: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    user_input_now[(e1, e2)] = (g1, g2)
        with c_tabla:
            st.markdown(f"<div class='titulo-posiciones'>📊 POSICIONES {zona}</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, user_input_now))

# SOLAPA 2: RESULTADOS REALES (SÓLO PUNTAJES)
with tab_r:
    if ahora < fecha_apertura_reales:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.warning(f"🔒 LA CARGA DE DATOS REALES SE HABILITARÁ EL 11 DE JUNIO A LAS 00:00.")
    else:
        st.markdown("<h2 style='color:#000000; text-align:center;'>🏆 RESULTADOS OFICIALES</h2>", unsafe_allow_html=True)
        resultados_reales = {}
        for zona, equipos in mundial.items():
            st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
            cr1, cr2 = st.columns([1, 1.2])
            with cr1:
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        e1, e2 = equipos[i], equipos[j]
                        cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                        with cols[0]: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                        gr1 = cols[1].number_input("", 0, 20, 0, key=f"r_{e1}_{e2}_{zona}", label_visibility="collapsed")
                        with cols[2]: st.markdown("<p style='text-align:center; font-weight:900;'>-</p>", unsafe_allow_html=True)
                        gr2 = cols[3].number_input("", 0, 20, 0, key=f"r2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                        with cols[4]: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                        resultados_reales[(e1, e2)] = (gr1, gr2)
            with cr2:
                st.markdown("<p class='titulo-posiciones'>📊 PUNTUACIÓN REAL</p>", unsafe_allow_html=True)
                df_real = pd.DataFrame({'Equipo': equipos, 'Puntos': 0}).set_index('Equipo')
                for (eq1, eq2), (v1, v2) in resultados_reales.items():
                    if v1 > 0 or v2 > 0 or (v1 == 0 and v2 == 0):
                        if v1 > v2: df_real.loc[eq1, 'Puntos'] += 3
                        elif v2 > v1: df_real.loc[eq2, 'Puntos'] += 3
                        else:
                            df_real.loc[eq1, 'Puntos'] += 1
                            df_real.loc[eq2, 'Puntos'] += 1
                st.table(df_real.sort_values(by='Puntos', ascending=False))

with tab_c:
    st.write("Comparativa de puntos según aciertos.")

st.divider()
if st.button("✅ Guardar Todo"):
    st.balloons()
