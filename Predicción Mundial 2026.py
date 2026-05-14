import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA DE ALTO CONTRASTE ---
st.set_page_config(page_title="Mundial 2026 - Predicción vs Realidad", page_icon="🏆", layout="wide")

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

    /* TÍTULOS DE ZONAS (NEGRO FUERTE) */
    .titulo-zona {
        font-family: 'Archivo Black', sans-serif;
        color: #000000 !important;
        font-size: 1.8rem !important;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 3px solid #1a472a;
        width: fit-content;
    }

    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }

    /* TÍTULO DE POSICIONES (MÁS GRANDE Y SIN FRANJA) */
    .titulo-posiciones {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    /* INPUTS MINI */
    div[data-testid="stNumberInput"] { width: 55px !important; }
    input { font-weight: 800 !important; color: #1a472a !important; }

    /* ESTILO DE LA TABLA */
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

# --- 2. LÓGICA DE DATOS ---
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
    tabla = pd.DataFrame({
        'Equipo': equipos, 
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            # Solo suma si hubo actividad (evita los 3 por defecto)
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
    nombre = st.text_input("👤 **TU NOMBRE:**")
    
    user_input_now = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c_partidos, c_tabla = st.columns([1, 1.2])
        
        with c_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with cols[0]: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    with cols[1]: g1 = st.number_input("", 0, 20, 0, key=f"f_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    with cols[2]: st.markdown("<p style='text-align:center; font-weight:900;'>-</p>", unsafe_allow_html=True)
                    with cols[3]: g2 = st.number_input("", 0, 20, 0, key=f"f2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    with cols[4]: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    user_input_now[(e1, e2)] = (g1, g2)
        
        with c_tabla:
            st.markdown(f"<div class='titulo-posiciones'>📊 POSICIONES {zona}</div>", unsafe_allow_html=True)
            df_final = calcular_df_estricto(equipos, user_input_now)
            st.table(df_final)

st.divider()
if st.button("✅ Finalizar Predicción"):
    st.balloons()
