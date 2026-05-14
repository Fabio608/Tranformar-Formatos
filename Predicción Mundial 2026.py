import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA DE IMPACTO ---
st.set_page_config(page_title="Mundial 2026 - Predicción vs Realidad", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Roboto:wght@400;700;900&display=swap');

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
        box-shadow: 0px 15px 50px rgba(0,0,0,0.8);
    }
    
    /* TÍTULO PRINCIPAL ULTRA NEGRITA */
    .titulo-principal {
        font-family: 'Playfair Display', serif;
        color: #1a472a;
        text-align: center;
        font-weight: 900;
        font-size: 4rem !important;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: -1px;
    }

    .subtitulo-app {
        text-align: center;
        color: #333;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 40px;
        border-bottom: 4px solid #1a472a;
        display: block;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }

    /* TEXTOS Y EQUIPOS */
    .nombre-equipo {
        font-family: 'Roboto', sans-serif;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }

    /* INPUTS */
    div[data-testid="stNumberInput"] { width: 75px !important; }
    input {
        font-size: 1.7rem !important;
        font-weight: 900 !important;
        color: #1a472a !important;
    }

    /* PESTAÑAS */
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.4rem !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='titulo-principal'>MUNDIAL 2026</h1>", unsafe_allow_html=True)
st.markdown("<span class='subtitulo-app'>PREDICCIÓN VS REALIDAD</span>", unsafe_allow_html=True)

# --- 2. LÓGICA DE TIEMPO ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)

# --- 3. DATOS ---
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

# Simulamos resultados reales cargados (Aquí es donde se actualizaría el mundial)
datos_oficiales = {
    ("🇦🇷 Argentina", "🇫🇷 Francia"): (2, 1),
    ("🇲🇽 México", "🇺🇸 EE.UU."): (1, 1),
}

def calcular_puntos(p_g1, p_g2, r_g1, r_g2):
    if p_g1 == r_g1 and p_g2 == r_g2: return 3 # Acierto exacto
    if (p_g1 > p_g2 and r_g1 > r_g2) or (p_g1 < p_g2 and r_g1 < r_g2) or (p_g1 == p_g2 and r_g1 == r_g2):
        return 1 # Acierto tendencia
    return 0

# --- 4. INTERFAZ ---
tab_pred, tab_real, tab_comp = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 TABLA DE PUNTOS"])

user_preds = {}

with tab_pred:
    nombre = st.text_input("👤 **TU NOMBRE:**", key="user_name")
    for zona, equipos in mundial.items():
        st.subheader(f"📍 {zona}")
        col_p, col_t = st.columns([1.5, 1])
        with col_p:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    c1, c2, c3, c4, c5 = st.columns([2, 0.8, 0.2, 0.8, 2])
                    with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"up_{e1}_{e2}")
                    with c3: st.markdown("<p style='text-align:center; font-weight:900;'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"up2_{e1}_{e2}")
                    with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    user_preds[(e1, e2)] = (g1, g2)

with tab_real:
    st.header("🏁 Marcadores Oficiales")
    for (e1, e2), (r1, r2) in datos_oficiales.items():
        st.write(f"✅ **{e1}** {r1} - {r2} **{e2}**")

with tab_comp:
    st.header("🎯 Comparativa y Puntaje")
    if not nombre:
        st.warning("Ingresá tu nombre en la primera pestaña para ver tu puntaje.")
    else:
        total_puntos = 0
        data_comp = []
        
        for (e1, e2), (p1, p2) in user_preds.items():
            if (e1, e2) in datos_oficiales:
                r1, r2 = datos_oficiales[(e1, e2)]
                puntos = calcular_puntos(p1, p2, r1, r2)
                total_puntos += puntos
                data_comp.append({
                    "Partido": f"{e1} vs {e2}",
                    "Tu Predicción": f"{p1}-{p2}",
                    "Resultado Real": f"{r1}-{r2}",
                    "Puntos Ganados": puntos
                })
        
        if data_comp:
            st.table(pd.DataFrame(data_comp))
            st.markdown(f"""
                <div style='background-color:#1a472a; padding:20px; border-radius:10px; text-align:center;'>
                    <h2 style='color:white; margin:0;'>TOTAL PUNTOS DE {nombre.upper()}: {total_puntos}</h2>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Aún no hay resultados oficiales cargados para comparar con tus predicciones.")

# Botón Final
st.divider()
if st.button("🚀 Finalizar y Compartir"):
    st.balloons()
    st.success("¡Copiá tus resultados y compartilos!")
