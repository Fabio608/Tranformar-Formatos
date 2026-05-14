import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 20px;
        padding: 40px;
    }
    .nombre-equipo { font-weight: 800; color: #1a472a; text-transform: uppercase; }
    button.step-up, button.step-down { display: none !important; }
    input { text-align: center !important; font-weight: 900 !important; color: #1a472a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATOS DEL MUNDIAL ---
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

# FUNCIÓN PARA CALCULAR TABLAS
def calcular_tabla(equipos, resultados):
    tabla = pd.DataFrame({'Equipo': equipos, 'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0}).set_index('Equipo')
    for res in resultados:
        e1, g1, e2, g2, jugado = res
        if jugado:
            tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
            tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
            else: tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    tabla['DG'] = tabla['GF'] - tabla['GC']
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 3. INTERFAZ DE PESTAÑAS ---
st.title("🏆 MUNDIAL 2026: REALIDAD VS PREDICCIÓN")

tab1, tab2 = st.tabs(["🔮 MI PREDICCIÓN (PRODE)", "📈 RESULTADOS REALES"])

with tab1:
    st.info("Cargá tus resultados aquí para generar tu mensaje de Prode.")
    nombre = st.text_input("👤 TU NOMBRE:", placeholder="Ej: Juan Pérez")
    predicciones_mensaje = []
    
    for zona, equipos in mundial.items():
        st.subheader(f"📅 {zona}")
        col1, col2 = st.columns([1.2, 1])
        res_prode = []
        with col1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    c_a, c_b, c_c, c_d, c_e = st.columns([2, 0.7, 0.3, 0.7, 2])
                    with c_a: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{equipos[i]}</p>", unsafe_allow_html=True)
                    with c_b: g1 = st.number_input("", 0, 20, 0, key=f"p_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c_c: st.markdown("<p style='text-align:center;'>-</p>", unsafe_allow_html=True)
                    with c_d: g2 = st.number_input("", 0, 20, 0, key=f"p2_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c_e: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{equipos[j]}</p>", unsafe_allow_html=True)
                    res_prode.append((equipos[i], g1, equipos[j], g2, (g1 > 0 or g2 > 0)))
                    if g1 > 0 or g2 > 0: predicciones_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
        with col2:
            st.dataframe(calcular_tabla(equipos, res_prode), use_container_width=True)

    if st.button("🚀 GENERAR MI PRODE"):
        if nombre:
            st.code(f"PRODE DE {nombre.upper()}\n" + "\n".join(predicciones_mensaje))
            st.balloons()

with tab2:
    st.header("📊 Tabla Oficial del Torneo")
    st.write("Esta sección muestra cómo van los grupos realmente.")
    
    # SIMULACIÓN DE DATOS REALES (Aquí es donde podés conectar un CSV o Sheet)
    # Por ahora, la dejamos fija para que veas cómo se vería:
    datos_reales = [
        ("🇲🇽 México", 2, "🇵🇦 Panamá", 0, True),
        ("🇦🇷 Argentina", 3, "🇯🇵 Japón", 1, True)
    ]
    
    for zona, equipos in mundial.items():
        st.subheader(f"Estado Oficial {zona}")
        # Filtramos solo los resultados que pertenecen a este grupo
        res_del_grupo = [r for r in datos_reales if r[0] in equipos]
        st.table(calcular_tabla(equipos, res_del_grupo))
