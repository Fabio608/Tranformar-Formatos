import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Predicción Mundial 2026", page_icon="⚽", layout="wide")

# Lógica de Tiempo (Argentina UTC-3)
AR = timezone(timedelta(hours=-3))
# El bloqueo de predicción es al iniciar el 11 de junio (00:00 hs)
fecha_limite_prediccion = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
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

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .soccer-icon {
        display: inline-block;
        animation: bounce 2s infinite ease-in-out;
        font-size: 2.5rem;
        margin: 0 8px;
    }

    .titulo-personalizado {
        font-family: 'Archivo Black', sans-serif;
        color: black;
        font-size: 3.2rem !important;
        text-align: center;
        margin: 0;
        -webkit-text-stroke: 1.5px white;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.2);
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
    .titulo-posiciones { font-family: 'Archivo Black', sans-serif; font-size: 1.6rem !important; color: #FF8C00 !important; text-align: center; margin-bottom: 10px; }

    [data-testid="stTable"] { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(255, 140, 0, 0.4) !important; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; font-family: 'Inter', sans-serif !important; border-bottom: 1px solid rgba(255, 140, 0, 0.3) !important; border-right: 1px solid rgba(255, 140, 0, 0.3) !important; text-align: center !important; padding: 12px !important; }
    [data-testid="stTable"] th { font-size: 1.1rem !important; font-weight: 700 !important; background-color: rgba(255, 140, 0, 0.1) !important; }
    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child { border-right: none !important; }

    div[data-testid="stNumberInput"] input { 
        background-color: #1a1a1a !important; 
        color: #FFD700 !important; 
        border: 2px solid #FF8C00 !important; 
        font-weight: 900 !important; 
        text-align: center !important;
    }
    </style>
    
    <div style="text-align: center; padding: 15px 0;">
        <span class="soccer-icon">⚽</span>
        <span class="titulo-personalizado">Predicción Mundial 2026</span>
        <span class="soccer-icon" style="animation-delay: 0.5s;">⚽</span>
    </div>
    """, unsafe_allow_html=True)

# --- 2. DATOS Y LÓGICA ---
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

def calcular_df_estricto(equipos, resultados_dict, es_prediccion=True):
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "Equipos"
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            # Solo procesamos si el usuario ingresó algún valor (no nulo)
            # Para que arranque en 0, verificamos si hubo interacción
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

# --- SOLAPA PREDICCIÓN ---
with tab_p:
    puede_editar_p = ahora < fecha_limite_prediccion
    if not puede_editar_p:
        st.error("🚫 El periodo de predicción ha finalizado (cerró el 10 de junio).")
    
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
                    # Arranca en None para que PJ y Pts sean 0 inicialmente
                    g1 = cols[1].number_input("", 0, 20, value=None, key=f"p_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_editar_p)
                    cols[2].markdown("<p style='text-align:center; color:white;'>-</p>", unsafe_allow_html=True)
                    g2 = cols[3].number_input("", 0, 20, value=None, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_editar_p)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    if g1 is not None and g2 is not None:
                        predicciones_usuario[(e1, e2)] = (g1, g2)
        with c2:
            st.markdown(f"<div class='titulo-posiciones'>📊 TU TABLA {zona}</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, predicciones_usuario))

# --- SOLAPA RESULTADOS REALES ---
with tab_r:
    puede_editar_r = ahora >= fecha_limite_prediccion
    if not puede_editar_r:
        st.warning("🔒 Los resultados oficiales podrán cargarse a partir del 11 de junio.")
    
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
                    g1 = c[1].number_input("", 0, 20, value=None, key=f"r_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_editar_r)
                    c[2].markdown("<p style='text-align:center; color:white;'>-</p>", unsafe_allow_html=True)
                    g2 = c[3].number_input("", 0, 20, value=None, key=f"r2_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_editar_r)
                    c[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    if g1 is not None and g2 is not None:
                        resultados_oficiales[(e1, e2)] = (g1, g2)
        with col2:
            st.markdown(f"<div class='titulo-posiciones'>📊 POSICIONES REALES {zona}</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, resultados_oficiales))

# --- SOLAPA PUNTAJE FINAL ---
with tab_c:
    total_gral = 0
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ Comparativa {zona}</div>", unsafe_allow_html=True)
        orden_p = calcular_df_estricto(equipos, predicciones_usuario).index.tolist()
        orden_r = calcular_df_estricto(equipos, resultados_oficiales).index.tolist()
        
        c_a, c_b, c_c = st.columns([1, 1, 1])
        puntos_z = 0
        for idx in range(len(equipos)):
            eq_p, eq_r = orden_p[idx], orden_r[idx]
            # Solo suma puntos si hay resultados reales cargados para esa zona
            if len(resultados_oficiales) > 0:
                pts = 2 if eq_p == eq_r else (1 if eq_p in orden_r[:2] and eq_r in orden_p[:2] else 0)
            else:
                pts = 0
            puntos_z += pts
            c_a.markdown(f"<p class='nombre-equipo'>{idx+1}° {eq_p}</p>", unsafe_allow_html=True)
            c_b.markdown(f"<p class='nombre-equipo'>{idx+1}° {eq_r}</p>", unsafe_allow_html=True)
            c_c.write(f"+{pts} pts")
        
        total_gral += puntos_z
        st.divider()
    
    st.markdown(f"<div style='background-color:#FF8C00; padding:20px; border-radius:15px; text-align:center;'><h1 style='color:black;'>PUNTAJE TOTAL: {total_gral}</h1></div>", unsafe_allow_html=True)
