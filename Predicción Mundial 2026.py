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
        font-family: 'Archivo Black', sans-serif;
        font-size: 1.6rem !important;
        color: #FF8C00 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    [data-testid="stTable"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 140, 0, 0.4) !important;
    }
    
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        border-bottom: 1px solid rgba(255, 140, 0, 0.3) !important;
        border-right: 1px solid rgba(255, 140, 0, 0.3) !important;
        text-align: center !important;
        padding: 12px !important;
    }
    
    [data-testid="stTable"] th {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child {
        border-right: none !important;
    }

    div[data-testid="stNumberInput"] input { 
        background-color: #2c2c2c !important; 
        color: white !important; 
        border: 1px solid #FF8C00 !important;
        font-weight: 800 !important;
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

def calcular_df_estricto(equipos, resultados_dict, simplificada=False):
    if simplificada:
        tabla = pd.DataFrame(0, index=equipos, columns=['Puntos'])
        tabla.index.name = "Equipos"
    else:
        tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
        tabla.index.name = "Equipos"
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            if g1 > 0 or g2 > 0:
                if not simplificada:
                    tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
                    tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
                    tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
                
                p_col = 'Puntos' if simplificada else 'Pts'
                if g1 > g2: tabla.loc[e1, p_col] += 3
                elif g2 > g1: tabla.loc[e2, p_col] += 3
                else:
                    tabla.loc[e1, p_col] += 1; tabla.loc[e2, p_col] += 1
                    
    sort_cols = ['Puntos'] if simplificada else ['Pts', 'DG', 'GF']
    return tabla.sort_values(by=sort_cols, ascending=False)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)

# --- 3. INTERFAZ ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

with tab_p:
    # NUEVA CORRECCIÓN: Bloqueo de predicción si ya empezó el mundial
    puede_predecir = ahora < fecha_apertura_reales
    
    if puede_predecir:
        st.text_input("👤 **TU NOMBRE:**", key="user_name")
    else:
        nombre_usu = st.session_state.get("user_name", "Participante")
        st.markdown(f"### 👤 Participante: {nombre_usu}")
        st.warning("🔒 Fase de pronósticos cerrada. ¡Mucha suerte con tus predicciones!")

    predicciones_usuario = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    cols[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    
                    # disabled=not puede_predecir bloquea los números después del 10/06
                    g1 = cols[1].number_input("", 0, 20, 0, key=f"p_{e1}_{e2}_{zona}", 
                                             label_visibility="collapsed", disabled=not puede_predecir)
                    cols[2].markdown("<p style='text-align:center; color:white;'>-</p>", unsafe_allow_html=True)
                    g2 = cols[3].number_input("", 0, 20, 0, key=f"p2_{e1}_{e2}_{zona}", 
                                             label_visibility="collapsed", disabled=not puede_predecir)
                    
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    predicciones_usuario[(e1, e2)] = (g1, g2)
        with c2:
            st.markdown(f"<div class='titulo-posiciones'>📊 POSICIONES {zona}</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, predicciones_usuario))

with tab_r:
    st.markdown("<h2 style='color:#FF8C00; text-align:center;'>📊 SEGUIMIENTO OFICIAL FIFA</h2>", unsafe_allow_html=True)
    es_fecha_edicion = ahora >= fecha_apertura_reales
    
    if not es_fecha_edicion:
        st.warning(f"🔒 MODO LECTURA: La carga de resultados se habilitará el 11 de junio.")
    
    resultados_oficiales = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 0.8])
        with col1:
            if es_fecha_edicion:
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        e1, e2 = equipos[i], equipos[j]
                        c = st.columns([2, 0.7, 0.2, 0.7, 2])
                        g1 = c[1].number_input("", 0, 20, 0, key=f"r_{e1}_{e2}_{zona}", label_visibility="collapsed")
                        c[2].write("-")
                        g2 = c[3].number_input("", 0, 20, 0, key=f"r2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                        c[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                        c[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                        resultados_oficiales[(e1, e2)] = (g1, g2)
            else:
                st.info(f"Los resultados reales se cargarán aquí al comenzar el Mundial.")

        with col2:
            st.markdown("<div class='titulo-posiciones'>📊 POSICIONES</div>", unsafe_allow_html=True)
            df_real = calcular_df_estricto(equipos, resultados_oficiales if es_fecha_edicion else {}, simplificada=True)
            st.table(df_real)

with tab_c:
    st.markdown("<h2 style='color:#FF8C00; text-align:center;'>🎯 TABLA GENERAL</h2>", unsafe_allow_html=True)
    st.write("Cálculo de aciertos y puntajes comparativos.")

st.divider()
if puede_predecir:
    if st.button("✅ Guardar Predicción"):
        st.balloons()
        st.success("¡Tu predicción ha sido guardada!")
else:
    st.button("✅ Guardar Predicción", disabled=True, help="El periodo de predicción terminó.")
