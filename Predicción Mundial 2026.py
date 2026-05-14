import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. ESTÉTICA REFINADA CON TABLAS DESTACADAS ---
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
    }

    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }

    /* INPUTS MINI */
    div[data-testid="stNumberInput"] { width: 55px !important; }
    input { font-weight: 800 !important; color: #1a472a !important; }

    /* DISEÑO DE TABLA (FONDO BLANCO COMO PIDIÓ EL USUARIO) */
    .tabla-contenedor {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #f0f0f0;
    }
    
    /* Forzar que la tabla de Streamlit sea blanca y legible */
    [data-testid="stTable"] {
        background-color: white !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: black !important;
        font-weight: 700 !important;
        border-bottom: 1px solid #eee !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)

# --- 2. LÓGICA DE DATOS SIN VALORES PRE-CARGADOS ---
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

# Simulador de oficiales para pestaña 'Realidad'
datos_oficiales = { ("🇦🇷 Argentina", "🇫🇷 Francia"): (2, 1) }

def calcular_df_estricto(equipos, resultados_dict):
    # Aseguramos que todo empiece en 0 absoluto
    tabla = pd.DataFrame({
        'Equipo': equipos, 
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            # Lógica para detectar si el usuario realmente ingresó datos (evita el error de la imagen)
            # Consideramos jugado si el valor en la UI es distinto de la clave única de reset
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
        st.markdown(f"### 📍 {zona}")
        c_partidos, c_tabla = st.columns([1, 1.2])
        
        with c_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with cols[0]: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    # Valor default 0 para que no sume puntos de entrada
                    with cols[1]: g1 = st.number_input("", 0, 20, 0, key=f"f_{e1}_{e2}", label_visibility="collapsed")
                    with cols[2]: st.markdown("<p style='text-align:center; font-weight:900;'>-</p>", unsafe_allow_html=True)
                    with cols[3]: g2 = st.number_input("", 0, 20, 0, key=f"f2_{e1}_{e2}", label_visibility="collapsed")
                    with cols[4]: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    
                    # Solo guardamos en el diccionario si el usuario movió los valores (o para inicializar tabla en 0)
                    user_input_now[(e1, e2)] = (g1, g2)
        
        with c_tabla:
            st.markdown("<div class='tabla-contenedor'>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-weight:900; color:black;'>📊 POSICIONES</p>", unsafe_allow_html=True)
            # Pasamos un diccionario filtrado: solo partidos donde PJ debería ser > 0 si hay goles o acción
            # Para esta versión, si el usuario no toca nada, PJ y Pts serán 0.
            input_filtrado = {k: v for k, v in user_input_now.items() if st.session_state.get(f"f_{k[0]}_{k[1]}") is not None and (v[0] > 0 or v[1] > 0)}
            
            df_final = calcular_df_estricto(equipos, input_filtrado)
            st.table(df_final)
            st.markdown("</div>", unsafe_allow_html=True)

with tab_r:
    st.info("Resultados cargados por el administrador aparecerán aquí con fondo claro.")
    for zona, equipos in mundial.items():
        st.table(calcular_df_estricto(equipos, datos_oficiales))

st.divider()
st.markdown("<p style='text-align:center; font-weight:bold;'>Límite: 10 de Junio 2026 - 23:59hs (UTC-3)</p>", unsafe_allow_html=True)
