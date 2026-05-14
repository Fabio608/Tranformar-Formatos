import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. ESTÉTICA REFINADA ---
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
        text-transform: uppercase;
    }

    .subtitulo-app {
        text-align: center;
        color: #000;
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 30px;
        border-bottom: 4px solid #1a472a;
        display: block;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }

    /* INPUTS MÁS PEQUEÑOS Y ESTÉTICOS (Como en image_d89186.jpg) */
    div[data-testid="stNumberInput"] {
        width: 60px !important;
    }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #f1f3f4 !important;
        border-radius: 10px !important;
        border: none !important;
    }
    input {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 5px !important;
    }

    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #333 !important;
    }

    /* TABLAS */
    .styled-table {
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)
st.markdown("<span class='subtitulo-app'>PREDICCIÓN VS REALIDAD</span>", unsafe_allow_html=True)

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

# Simulador de resultados oficiales (A actualizar manualmente)
datos_oficiales = {
    ("🇦🇷 Argentina", "🇫🇷 Francia"): (2, 1),
    ("🇲🇽 México", "🇺🇸 EE.UU."): (1, 1),
}

def calcular_df_tabla_completa(equipos, resultados_dict):
    # Columnas solicitadas: Equipo, Pts, PJ, GF, GC, DG
    tabla = pd.DataFrame({
        'Equipo': equipos, 
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            # Solo contamos si al menos uno puso un gol o se marcó como jugado
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

# --- 3. INTERFAZ POR PESTAÑAS ---
tab_pred, tab_real, tab_comp = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

user_preds_dict = {}

with tab_pred:
    nombre = st.text_input("👤 **TU NOMBRE:**", placeholder="Lionel Messi...")
    
    for zona, equipos in mundial.items():
        st.markdown(f"### 📍 {zona}")
        col_partidos, col_tabla = st.columns([1.2, 1])
        
        with col_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c1, c2, c3, c4, c5 = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"up_{e1}_{e2}", label_visibility="collapsed")
                    with c3: st.markdown("<p style='text-align:center; font-weight:bold; margin-top:5px;'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"up2_{e1}_{e2}", label_visibility="collapsed")
                    with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    user_preds_dict[(e1, e2)] = (g1, g2)
        
        with col_tabla:
            st.markdown("<p style='font-weight:800; color:#1a472a;'>📊 POSICIONES ESTIMADAS</p>", unsafe_allow_html=True)
            df_u = calcular_df_tabla_completa(equipos, user_preds_dict)
            st.dataframe(df_u, use_container_width=True)

with tab_real:
    st.header("🏁 Realidad del Torneo")
    for zona, equipos in mundial.items():
        st.subheader(f"{zona} - Oficial")
        col_r1, col_r2 = st.columns([1, 1.2])
        with col_r1:
            for (e1, e2), (r1, r2) in datos_oficiales.items():
                if e1 in equipos:
                    st.markdown(f"⚽ **{e1}** {r1} - {r2} **{e2}**")
        with col_r2:
            df_r = calcular_df_tabla_completa(equipos, datos_oficiales)
            st.dataframe(df_r, use_container_width=True)

with tab_comp:
    if not nombre:
        st.info("Completa tu nombre para ver el análisis de puntos.")
    else:
        st.header(f"🎯 Resumen para {nombre.upper()}")
        pts_partido = 0
        pts_posicion = 0
        
        for zona, equipos in mundial.items():
            # Comparación de tablas
            real_rank = calcular_df_tabla_completa(equipos, datos_oficiales).index.tolist()
            user_rank = calcular_df_tabla_completa(equipos, user_preds_dict).index.tolist()
            
            for idx in range(len(real_rank)):
                if real_rank[idx] == user_rank[idx]:
                    pts_posicion += 2
        
        for (e1, e2), (p1, p2) in user_preds_dict.items():
            if (e1, e2) in datos_oficiales:
                r1, r2 = datos_oficiales[(e1, e2)]
                if p1 == r1 and p2 == r2: pts_partido += 3
                elif (p1>p2 and r1>r2) or (p1<p2 and r1<r2) or (p1==p2 and r1==r2): pts_partido += 1
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Puntos Partidos", pts_partido)
        c2.metric("Puntos Posición", pts_posicion)
        c3.metric("TOTAL", pts_partido + pts_posicion)

st.divider()
if st.button("✅ Finalizar y Compartir"):
    st.balloons()
    st.success("¡Predicción lista! Ya puedes capturar pantalla o copiar tus resultados.")
