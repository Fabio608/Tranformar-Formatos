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
    .stApp { background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000"); background-size: cover; background-attachment: fixed; }
    .titulo-principal { font-family: 'Archivo Black', sans-serif; color: #FF8C00; text-align: center; font-size: 3.5rem !important; }
    .titulo-zona { font-family: 'Archivo Black', sans-serif; color: #FF8C00 !important; font-size: 1.5rem !important; border-bottom: 2px solid #FF8C00; margin-bottom: 10px; }
    .nombre-equipo { font-family: 'Inter', sans-serif; font-weight: 700; color: white; }
    [data-testid="stTable"] { background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 10px; border: 1px solid rgba(255, 140, 0, 0.4); }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATOS ---
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
    nombre_idx = "Equipos"
    col_puntos = 'Puntos' if simplificada else 'Pts'
    cols = [col_puntos] if simplificada else [col_puntos, 'PJ', 'GF', 'GC', 'DG']
    
    tabla = pd.DataFrame(0, index=equipos, columns=cols)
    tabla.index.name = nombre_idx
    
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos and (g1 > 0 or g2 > 0 or "r_" in str(st.session_state)): # Simplificación para detectar carga
            if not simplificada:
                tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
                tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
                tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
            if g1 > g2: tabla.loc[e1, col_puntos] += 3
            elif g2 > g1: tabla.loc[e2, col_puntos] += 3
            else: tabla.loc[e1, col_puntos] += 1; tabla.loc[e2, col_puntos] += 1
            
    return tabla.sort_values(by=[col_puntos], ascending=False)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 COMPARATIVA Y PUNTOS"])

# --- TAB PREDICCIÓN ---
with tab_p:
    puede_predecir = ahora < fecha_apertura_reales
    st.text_input("👤 **TU NOMBRE:**", key="user_name")
    pred_user = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                    g1 = cols[1].number_input("", 0, 10, 0, key=f"p_{e1}_{e2}_{zona}", disabled=not puede_predecir)
                    g2 = cols[3].number_input("", 0, 10, 0, key=f"p2_{e1}_{e2}_{zona}", disabled=not puede_predecir)
                    cols[0].write(e1); cols[4].write(e2)
                    pred_user[(e1, e2)] = (g1, g2)
        with c2:
            st.table(calcular_df_estricto(equipos, pred_user))

# --- TAB REALES ---
with tab_r:
    es_fecha_edicion = ahora >= fecha_apertura_reales
    res_oficial = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            if es_fecha_edicion:
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        e1, e2 = equipos[i], equipos[j]
                        cols = st.columns([2, 0.6, 0.2, 0.6, 2])
                        g1 = cols[1].number_input("", 0, 10, 0, key=f"r_{e1}_{e2}_{zona}")
                        g2 = cols[3].number_input("", 0, 10, 0, key=f"r2_{e1}_{e2}_{zona}")
                        res_oficial[(e1, e2)] = (g1, g2)
            else: st.info("Habilitado el 11 de Junio.")
        with c2:
            st.table(calcular_df_estricto(equipos, res_oficial, simplificada=True))

# --- TAB COMPARATIVA (LA NUEVA) ---
with tab_c:
    st.markdown("<h2 style='color:#FF8C00; text-align:center;'>📊 COMPARATIVA DE TABLAS</h2>", unsafe_allow_html=True)
    
    total_puntos_ganados = 0
    
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ Análisis {zona}</div>", unsafe_allow_html=True)
        
        # Obtenemos el orden de los equipos (el índice del DataFrame ya viene ordenado)
        orden_pred = calcular_df_estricto(equipos, pred_user).index.tolist()
        orden_real = calcular_df_estricto(equipos, res_oficial, simplificada=True).index.tolist()
        
        col_a, col_b, col_c = st.columns([1, 1, 1])
        
        col_a.write("**Tu Posición**")
        col_b.write("**Posición Real**")
        col_c.write("**Puntos Obtenidos**")
        
        puntos_zona = 0
        for i in range(len(equipos)):
            eq_pred = orden_pred[i]
            eq_real = orden_real[i]
            
            # Lógica de puntos:
            # Si el equipo que vos pusiste en posición i es el mismo que quedó en la realidad...
            if eq_pred == eq_real:
                puntos_item = 2  # Coincidencia total de posición
                icono = "✅"
            elif eq_pred in orden_real[:2] and eq_real in orden_pred[:2]:
                puntos_item = 1  # "Empate": Los dos clasificaron pero en distinto orden
                icono = "🌗"
            else:
                puntos_item = 0
                icono = "❌"
            
            puntos_zona += puntos_item
            
            col_a.write(f"{i+1}° {eq_pred}")
            col_b.write(f"{i+1}° {eq_real}")
            col_c.write(f"{icono} +{puntos_item} pts")
        
        total_puntos_ganados += puntos_zona
        st.write(f"**Subtotal {zona}: {puntos_zona} pts**")
        st.divider()

    # --- RESUMEN FINAL ---
    st.markdown(f"""
        <div style='background-color:#FF8C00; padding:20px; border-radius:15px; text-align:center;'>
            <h1 style='color:black; margin:0;'>SUMA TOTAL: {total_puntos_ganados} PUNTOS</h1>
            <p style='color:black; font-weight:bold;'>Basado en la coincidencia de posiciones entre tu predicción y la realidad.</p>
        </div>
    """, unsafe_allow_html=True)
