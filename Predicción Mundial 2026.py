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
        background-color: transparent !important; 
        padding: 30px 50px;
    }
    
    .titulo-principal {
        font-family: 'Archivo Black', sans-serif;
        color: #FF8C00; 
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 20px;
    }

    .titulo-zona {
        font-family: 'Archivo Black', sans-serif;
        color: #FF8C00 !important; 
        font-size: 1.8rem !important;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 3px solid #FF8C00;
        width: fit-content;
    }

    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important; 
    }

    .titulo-posiciones {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        color: #FF8C00 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    div[data-testid="stNumberInput"] { width: 60px !important; }
    input { 
        background-color: #2c2c2c !important; 
        color: white !important; 
        font-weight: 800 !important; 
        border: 1px solid #FF8C00 !important;
    }

    /* Estilo de las Tablas con Líneas Verticales */
    [data-testid="stTable"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 140, 0, 0.3) !important;
    }
    
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(255, 140, 0, 0.3) !important;
        border-right: 1px solid rgba(255, 140, 0, 0.2) !important;
        text-align: center !important;
    }
    
    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child {
        border-right: none !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FF8C00 !important;
        border-bottom-color: #FF8C00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)

# --- 2. DATOS DE GRUPOS ---
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

def calcular_df_estricto(equipos, resultados_dict):
    # Inicialización en 0
    tabla = pd.DataFrame({
        'Equipo': equipos, 
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        # Solo suma si al menos un input es mayor a 0 (evita el "3" automático si no hay datos)
        if e1 in equipos and e2 in equipos:
            if g1 > 0 or g2 > 0: 
                tabla.loc[e1, 'PJ'] += 1
                tabla.loc[e2, 'PJ'] += 1
                tabla.loc[e1, 'GF'] += g1
                tabla.loc[e1, 'GC'] += g2
                tabla.loc[e2, 'GF'] += g2
                tabla.loc[e2, 'GC'] += g1
                if g1 > g2: tabla.loc[e1, 'Pts'] += 3
                elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
                else:
                    tabla.loc[e1, 'Pts'] += 1
                    tabla.loc[e2, 'Pts'] += 1
                    
    tabla['DG'] = tabla['GF'] - tabla['GC']
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 3. INTERFAZ ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

with tab_p:
    st.text_input("👤 **TU NOMBRE:**", key="user_name")
    user_input_now = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with cols[0]: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    g1 = cols[1].number_input("", 0, 20, 0, key=f"p_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    with cols[2]: st.markdown("<p style='text-align:center; color:white;'>-</p>", unsafe_allow_html=True)
                    g2 = cols[3].number_input("", 0, 20, 0, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    with cols[4]: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    user_input_now[(e1, e2)] = (g1, g2)
        with c2:
            st.markdown(f"<div class='titulo-posiciones'>📊 POSICIONES {zona}</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, user_input_now))

with tab_r:
    if ahora < fecha_apertura_reales:
        st.info(f"🔒 LA CARGA DE DATOS REALES SE HABILITARÁ EL 11 DE JUNIO A LAS 00:00.")
    else:
        st.markdown("<h2 style='color:#FF8C00; text-align:center;'>🏆 RESULTADOS OFICIALES</h2>", unsafe_allow_html=True)

st.divider()
if st.button("✅ Guardar Predicción"):
    st.balloons()
