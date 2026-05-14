import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. ESTÉTICA REFINADA Y CONTRASTE ALTO ---
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
        margin-bottom: 0px;
    }

    /* EQUIPOS CON LETRAS INTENSAS (NEGRO PURO) */
    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 900 !important; /* Más intensidad */
        color: #000000 !important;  /* Negro absoluto */
    }

    /* INPUTS AÚN MÁS PEQUEÑOS */
    div[data-testid="stNumberInput"] {
        width: 50px !important; /* Más pequeño que antes */
    }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #f1f3f4 !important;
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
    }
    input {
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: #1a472a !important;
    }

    /* TABLAS CON CABECERAS OSCURAS */
    thead tr th {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:900; color:#000;'>PREDICCIÓN VS REALIDAD</p>", unsafe_allow_html=True)

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
# Inicializar con diccionarios vacíos para evitar cálculos erróneos antes de tiempo
if 'user_preds' not in st.session_state:
    st.session_state.user_preds = {}

# Datos oficiales para la pestaña de Realidad
datos_oficiales = {
    ("🇦🇷 Argentina", "🇫🇷 Francia"): (2, 1)
}

def calcular_df_tabla_limpia(equipos, resultados_dict):
    tabla = pd.DataFrame({
        'Equipo': equipos, 
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            # Solo sumar si el usuario interactuó (evita el error de la imagen d83104.jpg)
            if g1 > 0 or g2 > 0 or (g1 == 0 and g2 == 0): 
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
tab_pred, tab_real, tab_comp = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

with tab_pred:
    nombre = st.text_input("👤 **NOMBRE DEL PARTICIPANTE:**")
    
    current_preds = {}
    for zona, equipos in mundial.items():
        st.markdown(f"### 📍 {zona}")
        col_p, col_t = st.columns([1, 1.2])
        
        with col_p:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c1, c2, c3, c4, c5 = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"n_{e1}_{e2}", label_visibility="collapsed")
                    with c3: st.markdown("<p style='text-align:center; font-weight:bold;'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"n2_{e1}_{e2}", label_visibility="collapsed")
                    with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    current_preds[(e1, e2)] = (g1, g2)
        
        with col_t:
            st.markdown("<p style='font-weight:900; color:#000; text-align:center;'>📊 POSICIONES ESTIMADAS</p>", unsafe_allow_html=True)
            df_display = calcular_df_tabla_limpia(equipos, current_preds)
            st.table(df_display) # Usamos st.table para que las letras sean más firmes y claras

with tab_real:
    for zona, equipos in mundial.items():
        st.subheader(f"Oficial: {zona}")
        st.table(calcular_df_tabla_limpia(equipos, datos_oficiales))

with tab_comp:
    st.info("Aquí se mostrará la comparativa de puntos una vez que comiencen los partidos.")

if st.button("✅ Finalizar y Compartir"):
    st.balloons()
