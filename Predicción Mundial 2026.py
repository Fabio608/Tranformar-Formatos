import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Predicción Mundial 2026", page_icon="⚽", layout="wide")

AR = timezone(timedelta(hours=-3))
fecha_apertura_reales = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
ahora = datetime.now(AR)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), 
                    url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Animación de Pelotas Rebotando */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .soccer-icon {
        display: inline-block;
        animation: bounce 2s infinite ease-in-out;
        font-size: 3rem;
        margin: 0 10px;
    }

    /* Título Negro con Borde Blanco */
    .titulo-personalizado {
        font-family: 'Archivo Black', sans-serif;
        color: black;
        font-size: 4.5rem !important;
        text-align: center;
        margin: 0;
        /* Efecto de borde blanco (text-stroke) */
        -webkit-text-stroke: 2px white;
        text-shadow: 3px 3px 0px rgba(0,0,0,0.2);
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

    .nombre-equipo { font-family: 'Inter', sans-serif; font-size: 1.1rem !important; font-weight: 700 !important; color: #FFFFFF !important; }
    
    div[data-testid="stNumberInput"] input { 
        background-color: #1a1a1a !important; 
        color: #FFD700 !important; 
        border: 2px solid #FF8C00 !important; 
        font-weight: 900 !important; 
        text-align: center !important;
    }
    </style>
    
    <div style="text-align: center; padding: 20px 0;">
        <span class="soccer-icon">⚽</span>
        <span class="titulo-personalizado">Predicción Mundial 2026</span>
        <span class="soccer-icon" style="animation-delay: 0.5s;">⚽</span>
    </div>
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

def calcular_df_estricto(equipos, resultados_dict):
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "Equipos"
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
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
    st.text_input("👤 **NOMBRE DEL PARTICIPANTE:**", key="user_name")
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
                    g1 = cols[1].number_input("", 0, 20, 0, key=f"p_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    cols[2].markdown("<p style='text-align:center; color:white;'>-</p>", unsafe_allow_html=True)
                    g2 = cols[3].number_input("", 0, 20, 0, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    predicciones_usuario[(e1, e2)] = (g1, g2)
        with c2:
            st.table(calcular_df_estricto(equipos, predicciones_usuario))

with tab_r:
    resultados_oficiales = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.2])
        with col1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c = st.columns([2, 0.7, 0.2, 0.7, 2])
                    c[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    g1 = c[1].number_input("", 0, 20, 0, key=f"r_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    c[2].write("-")
                    g2 = c[3].number_input("", 0, 20, 0, key=f"r2_{e1}_{e2}_{zona}", label_visibility="collapsed")
                    c[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    resultados_oficiales[(e1, e2)] = (g1, g2)
        with col2:
            st.table(calcular_df_estricto(equipos, resultados_oficiales))

with tab_c:
    total_gral = 0
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ {zona}</div>", unsafe_allow_html=True)
        orden_p = calcular_df_estricto(equipos, predicciones_usuario).index.tolist()
        orden_r = calcular_df_estricto(equipos, resultados_oficiales).index.tolist()
        c_a, c_b, c_c = st.columns([1, 1, 1])
        puntos_z = 0
        for idx in range(len(equipos)):
            eq_p, eq_r = orden_p[idx], orden_r[idx]
            pts = 2 if eq_p == eq_r else (1 if eq_p in orden_r[:2] and eq_r in orden_p[:2] else 0)
            puntos_z += pts
            c_a.markdown(f"{idx+1}° {eq_p}")
            c_b.markdown(f"{idx+1}° {eq_r}")
            c_c.write(f"+{pts} pts")
        total_gral += puntos_z
        st.divider()
    st.markdown(f"<div style='background-color:#FF8C00; padding:20px; border-radius:15px; text-align:center;'><h1 style='color:black;'>TOTAL: {total_gral} PUNTOS</h1></div>", unsafe_allow_html=True)
