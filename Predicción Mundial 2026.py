import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Mundial 2026 - Comparativa", page_icon="🏆", layout="wide")

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
    .titulo-principal { font-family: 'Archivo Black', sans-serif; color: #FF8C00; text-align: center; font-size: 3.5rem !important; margin-bottom: 20px; }
    .titulo-zona { font-family: 'Archivo Black', sans-serif; color: #FF8C00 !important; font-size: 1.8rem !important; margin-top: 20px; margin-bottom: 15px; border-bottom: 3px solid #FF8C00; width: fit-content; }
    .nombre-equipo { font-family: 'Inter', sans-serif; font-size: 1.1rem !important; font-weight: 700 !important; color: #FFFFFF !important; }
    .titulo-posiciones { font-family: 'Archivo Black', sans-serif; font-size: 1.6rem !important; color: #FF8C00 !important; text-align: center; margin-bottom: 10px; }
    [data-testid="stTable"] { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(255, 140, 0, 0.4) !important; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; font-family: 'Inter', sans-serif !important; border-bottom: 1px solid rgba(255, 140, 0, 0.3) !important; border-right: 1px solid rgba(255, 140, 0, 0.3) !important; text-align: center !important; padding: 12px !important; }
    [data-testid="stTable"] th { font-size: 1.2rem !important; font-weight: 700 !important; background-color: rgba(255, 140, 0, 0.1) !important; }
    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child { border-right: none !important; }
    div[data-testid="stNumberInput"] input { background-color: #2c2c2c !important; color: white !important; border: 1px solid #FF8C00 !important; font-weight: 800 !important; }
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

def calcular_df_estricto(equipos, resultados_dict):
    # Restauradas columnas Pts y PJ
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "Equipos"
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            # Solo procesamos si hay algún gol cargado
            if g1 > 0 or g2 > 0 or (f"r_{e1}_{e2}" in st.session_state and st.session_state[f"r_{e1}_{e2}"] is not None):
                tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
                tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
                tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
                tabla.loc[e1, 'DG'] = tabla.loc[e1, 'GF'] - tabla.loc[e1, 'GC']
                tabla.loc[e2, 'DG'] = tabla.loc[e2, 'GF'] - tabla.loc[e2, 'GC']
                
                if g1 > g2: tabla.loc[e1, 'Pts'] += 3
                elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
                else: tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
                    
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)

# --- 3. INTERFAZ ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

with tab_p:
    puede_predecir = ahora < fecha_apertura_reales
    if puede_predecir:
        faltan = fecha_apertura_reales - ahora
        st.info(f"⏳ **TIEMPO RESTANTE PARA EDITAR:** {faltan.days} días, {faltan.seconds//3600} h y {(faltan.seconds//60)%60} m.")
        st.text_input("👤 **TU NOMBRE:**", key="user_name")
    else:
        st.error("🚫 **TIEMPO AGOTADO:** El periodo de edición finalizó.")

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
                    g1 = cols[1].number_input("", 0, 20, 0, key=f"p_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_predecir)
                    cols[2].markdown("<p style='text-align:center; color:white;'>-</p>", unsafe_allow_html=True)
                    g2 = cols[3].number_input("", 0, 20, 0, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_predecir)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    predicciones_usuario[(e1, e2)] = (g1, g2)
        with c2:
            st.markdown(f"<div class='titulo-posiciones'>📊 POSICIONES {zona}</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, predicciones_usuario))

with tab_r:
    st.markdown("<h2 style='color:#FF8C00; text-align:center;'>📊 SEGUIMIENTO OFICIAL FIFA</h2>", unsafe_allow_html=True)
    es_fecha_edicion = ahora >= fecha_apertura_reales
    if not es_fecha_edicion:
        st.warning(f"🔒 La carga de resultados se habilitará el 11 de junio.")
    
    resultados_oficiales = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.2]) # Restaurado el ancho para la tabla
        with col1:
            if es_fecha_edicion:
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
            else:
                st.info("Habilitado al comenzar el Mundial.")
        with col2:
            st.markdown("<div class='titulo-posiciones'>📊 POSICIONES REALES</div>", unsafe_allow_html=True)
            st.table(calcular_df_estricto(equipos, resultados_oficiales)) # Tabla completa restaurada

with tab_c:
    st.markdown("<h2 style='color:#FF8C00; text-align:center;'>🎯 COMPARATIVA Y PUNTAJE FINAL</h2>", unsafe_allow_html=True)
    total_gral = 0
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ {zona}</div>", unsafe_allow_html=True)
        orden_p = calcular_df_estricto(equipos, predicciones_usuario).index.tolist()
        orden_r = calcular_df_estricto(equipos, resultados_oficiales).index.tolist()
        
        c_a, c_b, c_c = st.columns([1, 1, 1])
        c_a.markdown("**TU PREDICCIÓN**")
        c_b.markdown("**REALIDAD**")
        c_c.markdown("**PUNTOS**")
        
        puntos_z = 0
        for idx in range(len(equipos)):
            eq_p, eq_r = orden_p[idx], orden_r[idx]
            if eq_p == eq_r: pts, ico = 2, "✅"
            elif eq_p in orden_r[:2] and eq_r in orden_p[:2]: pts, ico = 1, "🌗"
            else: pts, ico = 0, "❌"
            puntos_z += pts
            c_a.markdown(f"<p class='nombre-equipo'>{idx+1}° {eq_p}</p>", unsafe_allow_html=True)
            c_b.markdown(f"<p class='nombre-equipo'>{idx+1}° {eq_r}</p>", unsafe_allow_html=True)
            c_c.write(f"{ico} +{pts}")
        
        total_gral += puntos_z
        st.write(f"**Subtotal {zona}: {puntos_z} pts**")
        st.divider()

    st.markdown(f"<div style='background-color:#FF8C00; padding:20px; border-radius:15px; text-align:center;'><h1 style='color:black;'>SUMA TOTAL: {total_gral} PUNTOS</h1></div>", unsafe_allow_html=True)
