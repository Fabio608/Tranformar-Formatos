import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. ESTÉTICA DE MÁXIMA LEGIBILIDAD Y DISEÑO PROFESIONAL ---
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
        padding: 50px;
        box-shadow: 0px 15px 50px rgba(0,0,0,0.9);
    }
    
    .titulo-principal {
        font-family: 'Archivo Black', sans-serif;
        color: #1a472a;
        text-align: center;
        font-size: 4rem !important;
        margin-bottom: 0px;
        text-transform: uppercase;
        text-shadow: 3px 3px 0px #e0e0e0;
    }

    .subtitulo-app {
        text-align: center;
        color: #000000;
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        margin-bottom: 40px;
        border-bottom: 6px solid #1a472a;
        display: block;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        padding-bottom: 5px;
    }

    /* EQUIPOS Y TEXTOS EN NEGRO ABSOLUTO */
    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }

    h3 { color: #000000 !important; font-weight: 900 !important; }

    /* ESTILO PESTAÑAS */
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        color: #333333 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #1a472a !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)
st.markdown("<span class='subtitulo-app'>PREDICCIÓN VS REALIDAD</span>", unsafe_allow_html=True)

# --- 2. DATOS Y MUNDIAL ---
AR = timezone(timedelta(hours=-3))
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

# RESULTADOS REALES (Aquí cargarás lo que pase en el mundial)
datos_oficiales = {
    ("🇦🇷 Argentina", "🇫🇷 Francia"): (2, 1),
    ("🇲🇽 México", "🇺🇸 EE.UU."): (1, 1),
}

def calcular_df_tabla(equipos, resultados_dict):
    tabla = pd.DataFrame({'Equipo': equipos, 'Pts': 0, 'PJ': 0, 'DG': 0}).set_index('Equipo')
    for (e1, e2), (g1, g2) in resultados_dict.items():
        if e1 in equipos and e2 in equipos:
            tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'DG'] += (g1 - g2); tabla.loc[e2, 'DG'] += (g2 - g1)
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g2 > g1: tabla.loc[e2, 'Pts'] += 3
            else: 
                tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    return tabla.sort_values(by=['Pts', 'DG'], ascending=False)

# --- 3. INTERFAZ ---
tab_pred, tab_real, tab_comp = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

user_preds_dict = {}

with tab_pred:
    nombre = st.text_input("👤 **TU NOMBRE:**", key="user_name", placeholder="Ej: Lionel")
    for zona, equipos in mundial.items():
        st.subheader(f"📍 {zona}")
        col_p, col_t = st.columns([1.5, 1])
        with col_p:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c1, c2, c3, c4, c5 = st.columns([2, 0.8, 0.2, 0.8, 2])
                    with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"p_{e1}_{e2}")
                    with c3: st.markdown("<p style='text-align:center; font-weight:900;'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"p2_{e1}_{e2}")
                    with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    user_preds_dict[(e1, e2)] = (g1, g2)
        with col_t:
            st.markdown("**📊 TU TABLA PROVISORIA**")
            st.dataframe(calcular_df_tabla(equipos, user_preds_dict), use_container_width=True)

with tab_real:
    st.header("🏁 Marcadores y Posiciones Oficiales")
    for zona, equipos in mundial.items():
        st.subheader(f"Estado {zona}")
        col_rp, col_rt = st.columns([1, 1])
        with col_rp:
            for (e1, e2), (r1, r2) in datos_oficiales.items():
                if e1 in equipos: st.markdown(f"✅ **{e1}** {r1} — {r2} **{e2}**")
        with col_rt:
            st.dataframe(calcular_df_tabla(equipos, datos_oficiales), use_container_width=True)

with tab_comp:
    if not nombre:
        st.warning("Escribe tu nombre en la pestaña de Predicción.")
    else:
        st.header(f"📊 Puntaje de {nombre.upper()}")
        p_partidos, p_posiciones = 0, 0
        detalles = []

        for zona, equipos in mundial.items():
            st.subheader(f"Comparativa {zona}")
            orden_real = calcular_df_tabla(equipos, datos_oficiales).index.tolist()
            orden_pred = calcular_df_tabla(equipos, user_preds_dict).index.tolist()
            
            c1, c2 = st.columns(2)
            c1.write("**Tu Predicción:** " + " > ".join(orden_pred))
            c2.write("**Realidad:** " + " > ".join(orden_real))
            
            for idx in range(len(orden_real)):
                if orden_real[idx] == orden_pred[idx]:
                    p_posiciones += 2
                    st.success(f"🎯 Acertaste el {idx+1}° puesto de {orden_real[idx]} (+2 pts)")

        # Cálculo de puntos por partido
        for (e1, e2), (p1, p2) in user_preds_dict.items():
            if (e1, e2) in datos_oficiales:
                r1, r2 = datos_oficiales[(e1, e2)]
                pts = 3 if (p1 == r1 and p2 == r2) else (1 if (p1>p2 and r1>r2) or (p1<p2 and r1<r2) or (p1==p2 and r1==r2) else 0)
                p_partidos += pts
                detalles.append({"Partido": f"{e1}-{e2}", "Tu Pred.": f"{p1}-{p2}", "Real": f"{r1}-{r2}", "Pts": pts})

        st.divider()
        st.metric("PUNTOS TOTALES", p_partidos + p_posiciones, f"Partidos: {p_partidos} | Posiciones: {p_posiciones}")
        if detalles: st.table(pd.DataFrame(detalles))

st.divider()
if st.button("🚀 Finalizar y Compartir"):
    st.balloons()
    st.success("¡Progreso completado!")
