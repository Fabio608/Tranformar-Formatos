import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Predicción Mundial 2026", page_icon="⚽", layout="wide")

AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
ahora = datetime.now(AR)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), 
                    url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }

    .titulo-personalizado {
        font-family: 'Archivo Black', sans-serif;
        color: white;
        font-size: 3rem !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    .titulo-zona { 
        font-family: 'Archivo Black', sans-serif; 
        color: #FF8C00 !important; 
        font-size: 1.6rem !important; 
        margin-top: 30px;
        padding-left: 10px;
        border-left: 5px solid #FF8C00;
    }

    .nombre-equipo { font-family: 'Inter', sans-serif; font-size: 1.05rem !important; font-weight: 700 !important; color: #FFFFFF !important; }

    /* --- TABLA DE POSICIONES ESTILIZADA --- */
    [data-testid="stTable"] { 
        background-color: rgba(255, 255, 255, 0.03) !important; 
        backdrop-filter: blur(10px);
        border-radius: 12px !important; 
        border: 1px solid rgba(255, 140, 0, 0.3) !important; 
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stTable"] thead tr th {
        background-color: rgba(255, 140, 0, 0.2) !important;
        color: #FF8C00 !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.85rem !important;
        border-bottom: 2px solid #FF8C00 !important;
    }

    [data-testid="stTable"] td { 
        color: #E0E0E0 !important; 
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        font-size: 0.95rem !important;
        padding: 12px !important;
    }

    [data-testid="stTable"] tr:hover {
        background-color: rgba(255, 140, 0, 0.05) !important;
    }

    /* --- SOLUCIÓN DEFINITIVA A image_cb7d44.png --- */
    /* Eliminar flechas en todos los navegadores */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none !important;
      margin: 0 !important;
    }
    input[type=number] {
      -moz-appearance: textfield !important;
    }

    /* Ocultar botones internos de Streamlit (+, -, X) */
    div[data-testid="stNumberInput"] button {
        display: none !important;
    }
    
    /* Limpieza total del contenedor de input */
    .stNumberInput div div {
        background-color: transparent !important;
    }

    div[data-testid="stNumberInput"] input { 
        background-color: #0e0e0e !important; 
        color: #FFD700 !important; 
        border: 1px solid #FF8C00 !important; 
        border-radius: 8px !important;
        font-weight: 800 !important; 
        font-size: 1.2rem !important;
        text-align: center !important;
        height: 45px !important;
    }

    /* Ocultar cualquier botón de 'clear' o 'X' por encima */
    svg[class^="st-"] { display: none !important; } 
    button[title="Clear value"] { display: none !important; }
    div[data-baseweb="input"] > div:last-child { display: none !important; }

    </style>
    
    <div class="titulo-personalizado">Prode Mundial 2026</div>
    """, unsafe_allow_html=True)

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

def calcular_df(equipos, resultados_dict):
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "EQUIPOS"
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if g1 is not None and g2 is not None:
            tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
            tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
            tabla.loc[e1, 'DG'] = tabla.loc[e1, 'GF'] - tabla.loc[e1, 'GC']
            tabla.loc[e2, 'DG'] = tabla.loc[e2, 'GF'] - tabla.loc[e2, 'GC']
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
            else: tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 3. INTERFAZ ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 PUNTAJE FINAL"])

with tab_p:
    puede_p = ahora < fecha_limite
    st.info("📅 Predicciones abiertas hasta el inicio del mundial.")
    st.text_input("👤 NOMBRE DEL PARTICIPANTE:", key="user_name")
    
    dict_p = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>{zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.1, 1])
        with c1:
            st.write("") # Espaciador
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    cols[0].markdown(f"<p class='nombre-equipo' style='text-align:right; margin-top:10px;'>{e1}</p>", unsafe_allow_html=True)
                    v1 = cols[1].number_input("", 0, 20, value=None, key=f"p1_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_p)
                    cols[2].markdown("<p style='text-align:center; color:#FF8C00; font-weight:bold; margin-top:10px;'>-</p>", unsafe_allow_html=True)
                    v2 = cols[3].number_input("", 0, 20, value=None, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_p)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left; margin-top:10px;'>{e2}</p>", unsafe_allow_html=True)
                    dict_p[(e1, e2)] = (v1, v2)
        with c2:
            st.table(calcular_df(equipos, dict_p))
    
    st.button("💾 Guardar Predicción", disabled=not puede_p, use_container_width=True)

# (Las demás solapas mantienen la misma lógica de cálculo)
