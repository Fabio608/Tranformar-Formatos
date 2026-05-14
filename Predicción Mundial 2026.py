import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Predicción Mundial 2026", page_icon="⚽", layout="wide")

AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
ahora = datetime.now(AR)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;700;900&display=swap');
    .stApp { background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000"); background-size: cover; background-attachment: fixed; }
    .titulo-personalizado { font-family: 'Archivo Black', sans-serif; color: black; font-size: 3rem !important; text-align: center; -webkit-text-stroke: 1.5px white; }
    .titulo-zona { font-family: 'Archivo Black', sans-serif; color: #FF8C00 !important; font-size: 1.8rem !important; border-bottom: 3px solid #FF8C00; width: fit-content; margin-bottom: 15px; }
    .nombre-equipo { font-family: 'Inter', sans-serif; font-size: 1.1rem !important; font-weight: 700 !important; color: #FFFFFF !important; }
    [data-testid="stTable"] { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(255, 140, 0, 0.4) !important; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; text-align: center !important; border-bottom: 1px solid rgba(255, 140, 0, 0.2) !important; }
    div[data-testid="stNumberInput"] input { background-color: #1a1a1a !important; color: #FFD700 !important; border: 2px solid #FF8C00 !important; font-weight: 900 !important; text-align: center !important; }
    </style>
    <div style="text-align: center; padding: 10px;">
        <h1 class="titulo-personalizado">Predicción Mundial 2026</h1>
    </div>
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

def calcular_tabla(equipos, resultados):
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "Equipos"
    for (e1, e2), (g1, g2) in resultados.items():
        # Solo procesa si ambos campos tienen valor y no son nulos por defecto
        if g1 != -1 and g2 != -1:
            tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
            tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
            tabla.loc[e1, 'DG'] = tabla.loc[e1, 'GF'] - tabla.loc[e1, 'GC']
            tabla.loc[e2, 'DG'] = tabla.loc[e2, 'GF'] - tabla.loc[e2, 'GC']
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
            else: tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 PUNTAJE FINAL"])

# --- SOLAPA PREDICCIÓN ---
with tab_p:
    puede_p = ahora < fecha_limite
    st.info(f"📅 Fecha límite para editar: 10 de Junio de 2026.")
    st.text_input("👤 **Nombre:**", key="user_name")
    
    dict_p = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        col_in, col_tab = st.columns([1, 1.2])
        with col_in:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c = st.columns([2, 0.7, 0.2, 0.7, 2])
                    c[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    # Usamos -1 como bandera interna para "vacío" y que la tabla sea 0
                    v1 = c[1].number_input("", -1, 20, value=-1, key=f"p1_{e1}_{e2}", label_visibility="collapsed", disabled=not puede_p)
                    c[2].write("-")
                    v2 = c[3].number_input("", -1, 20, value=-1, key=f"p2_{e1}_{e2}", label_visibility="collapsed", disabled=not puede_p)
                    c[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    dict_p[(e1, e2)] = (v1, v2)
        with col_tab:
            st.table(calcular_tabla(equipos, dict_p))
    
    if st.button("✅ Finalizar Resultados", disabled=not puede_p):
        st.success("¡Predicción guardada con éxito!")

# --- SOLAPA RESULTADOS REALES ---
with tab_r:
    puede_r = ahora >= fecha_limite
    if not puede_r:
        st.warning("🔒 Esta sección se habilitará el 11 de junio de 2026.")
    
    dict_r = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        col_in, col_tab = st.columns([1, 1.2])
        with col_in:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c = st.columns([2, 0.7, 0.2, 0.7, 2])
                    c[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    v1 = c[1].number_input("", -1, 20, value=-1, key=f"r1_{e1}_{e2}", label_visibility="collapsed", disabled=not puede_r)
                    c[2].write("-")
                    v2 = c[3].number_input("", -1, 20, value=-1, key=f"r2_{e1}_{e2}", label_visibility="collapsed", disabled=not puede_r)
                    c[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    dict_r[(e1, e2)] = (v1, v2)
        with col_tab:
            st.table(calcular_tabla(equipos, dict_r))

# --- SOLAPA PUNTAJE ---
with tab_c:
    total = 0
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ {zona}</div>", unsafe_allow_html=True)
        t_p = calcular_tabla(equipos, dict_p).index.tolist()
        t_r = calcular_tabla(equipos, dict_r).index.tolist()
        
        ca, cb, cc = st.columns(3)
        for idx in range(4):
            pts = 2 if t_p[idx] == t_r[idx] else (1 if t_p[idx] in t_r[:2] and t_r[idx] in t_p[:2] else 0)
            total += pts
            ca.write(f"{idx+1}° {t_p[idx]}")
            cb.write(f"Real: {t_r[idx]}")
            cc.write(f"+{pts} pts")
    st.markdown(f"<div style='background:#FF8C00; padding:20px; border-radius:10px; text-align:center;'><h2 style='color:black;'>PUNTOS TOTALES: {total}</h2></div>", unsafe_allow_html=True)
