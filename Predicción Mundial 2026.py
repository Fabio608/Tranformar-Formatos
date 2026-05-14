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
    
    .titulo-principal {
        font-family: 'Archivo Black', sans-serif;
        color: #FF8C00; 
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 20px;
    }

    /* Color de etiqueta 'Tu Nombre' */
    .stTextInput label p { color: white !important; font-weight: 700 !important; }

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

    .titulo-posiciones-mini {
        font-family: 'Archivo Black', sans-serif;
        font-size: 1.5rem !important;
        color: #FF8C00 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Estilo de la tabla imagen image_cd4b3b.png */
    [data-testid="stTable"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 140, 0, 0.4) !important;
    }
    
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        font-size: 1.1rem !important;
        border-bottom: 1px solid rgba(255, 140, 0, 0.3) !important;
        border-right: 1px solid rgba(255, 140, 0, 0.3) !important; /* Línea vertical */
        text-align: center !important;
        padding: 12px !important;
    }
    
    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child {
        border-right: none !important;
    }

    input { 
        background-color: #2c2c2c !important; 
        color: white !important; 
        border: 1px solid #FF8C00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

def calcular_puntos_reales(equipos, dict_resultados):
    tabla = pd.DataFrame({'Equipo': equipos, 'Pts': 0}).set_index('Equipo')
    for (e1, e2), (g1, g2) in dict_resultados.items():
        if e1 in equipos and e2 in equipos:
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
            elif g1 == g2 and (g1 != 0 or g2 != 0): # Empate con goles cargados
                tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    return tabla.sort_values(by='Pts', ascending=False)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)

# --- 3. INTERFAZ ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

with tab_p:
    st.text_input("👤 **TU NOMBRE:**", key="user_name")
    st.info("Sección de predicción activa.")

with tab_r:
    st.markdown("<h2 style='color:#FF8C00; text-align:center;'>📊 SEGUIMIENTO OFICIAL FIFA</h2>", unsafe_allow_html=True)
    
    es_fecha_edicion = ahora >= fecha_apertura_reales
    
    if not es_fecha_edicion:
        st.warning(f"🔒 MODO LECTURA: La edición se habilitará el 11 de junio.")
    else:
        st.success(f"🔓 MODO EDICIÓN ACTIVO: Cargando resultados oficiales.")

    # Diccionario para guardar resultados reales
    resultados_oficiales = {}

    # Generar todos los grupos
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        col_input, col_tabla = st.columns([1, 1])
        
        with col_input:
            if es_fecha_edicion:
                st.write("📝 CARGAR PARTIDOS:")
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        e1, e2 = equipos[i], equipos[j]
                        c = st.columns([2, 1, 0.3, 1, 2])
                        g1 = c[1].number_input("", 0, 20, 0, key=f"r_{e1}_{e2}_{zona}", label_visibility="collapsed")
                        c[2].write("-")
                        g2 = c[3].number_input("", 0, 20, 0, key=f"r2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                        c[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                        c[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                        resultados_oficiales[(e1, e2)] = (g1, g2)
            else:
                st.info("Los campos de carga aparecerán aquí el 11/06.")

        with col_tabla:
            st.markdown("<div class='titulo-posiciones-mini'>📊 POSICIONES</div>", unsafe_allow_html=True)
            df_zona = calcular_puntos_reales(equipos, resultados_oficiales if es_fecha_edicion else {})
            st.table(df_zona)

with tab_c:
    st.write("Cálculo de puntajes comparativos próximamente.")
