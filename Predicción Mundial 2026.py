import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA DE ALTO CONTRASTE ---
st.set_page_config(page_title="Mundial 2026 - Predicción vs Realidad", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    /* Fondo con overlay para legibilidad */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Contenedor Principal */
    .main .block-container {
        background: rgba(255, 255, 255, 1.0); /* Blanco puro para máximo contraste */
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    
    /* TEXTOS Y COLORES */
    .nombre-equipo {
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        color: #000000 !important; /* Negro para equipos */
        text-transform: uppercase;
    }

    .guion {
        font-size: 1.6rem;
        font-weight: 900;
        color: #1a472a;
        text-align: center;
    }

    /* INPUTS DE GOLES */
    button.step-up, button.step-down { display: none !important; }
    div[data-testid="stNumberInput"] { width: 65px !important; margin: 0 auto; }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        border: 2px solid #1a472a !important;
        border-radius: 10px !important;
    }
    input {
        text-align: center !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: #1a472a !important;
    }

    /* TÍTULOS */
    h1 { color: #1a472a; text-align: center; font-weight: 900; font-size: 3.2rem !important; }
    h2, h3 { color: #1a472a !important; font-weight: 800 !important; }
    
    /* PESTAÑAS (TABS) */
    .stTabs [data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        color: #444 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1a472a !important;
        border-bottom-color: #1a472a !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏆 Mundial 2026 - Predicción vs Realidad</h1>", unsafe_allow_html=True)

# --- 2. LÓGICA DE TIEMPO (UTC-3 Argentina) ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)
tiempo_restante = fecha_limite - ahora

# --- 3. DATOS Y CÁLCULOS ---
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

# --- 4. INTERFAZ ---
if ahora > fecha_limite:
    st.error("❌ El plazo de entrega finalizó el 10 de junio a las 23:59 (Hora Local).")
else:
    tab_pred, tab_real = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES"])

    with tab_pred:
        st.markdown(f"⏳ **TIEMPO RESTANTE:** {tiempo_restante.days} días, {tiempo_restante.seconds//3600} horas.")
        nombre = st.text_input("👤 **TU NOMBRE O APODO:**", placeholder="Escribe aquí...")
        
        predicciones_mensaje = []

        for zona, equipos in mundial.items():
            st.subheader(f"📍 {zona}")
            col_partidos, col_tabla = st.columns([1.3, 1])
            res_usuario = []
            
            with col_partidos:
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        c1, c2, c3, c4, c5 = st.columns([2, 0.7, 0.3, 0.7, 2])
                        with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{equipos[i]}</p>", unsafe_allow_html=True)
                        with c2: g1 = st.number_input("", 0, 20, 0, key=f"u_{zona}_{i}_{j}", label_visibility="collapsed")
                        with c3: st.markdown("<p class='guion'>-</p>", unsafe_allow_html=True)
                        with c4: g2 = st.number_input("", 0, 20, 0, key=f"u2_{zona}_{i}_{j}", label_visibility="collapsed")
                        with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{equipos[j]}</p>", unsafe_allow_html=True)
                        
                        jugado = (g1 > 0 or g2 > 0)
                        res_usuario.append((equipos[i], g1, equipos[j], g2, jugado))
                        if jugado: predicciones_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
            
            with col_tabla:
                st.markdown("**📊 TU TABLA ESTIMADA**")
                tabla_est = calcular_tabla(equipos, res_usuario)
                st.dataframe(tabla_est.style.highlight_max(subset=['Pts'], color='#c8e6c9'), use_container_width=True)

        st.divider()
        if st.button("✅ Finalizar y Compartir"):
            if nombre and predicciones_mensaje:
                resumen = f"🏆 PREDICCIÓN MUNDIAL 2026\n👤 JUGADOR: {nombre.upper()}\n" + "="*25 + "\n"
                resumen += "\n".join(predicciones_mensaje)
                st.success("¡Copiá y pegá este mensaje en tu grupo!")
                st.code(resumen, language="text")
                st.balloons()
            else:
                st.warning("⚠️ Asegurate de poner tu nombre y al menos un resultado.")

    with tab_real:
        st.header("🏁 Resultados Oficiales del Torneo")
        st.info("Aquí verás los resultados cargados oficialmente a medida que ocurran.")
        
        # Ejemplo de datos reales (esto lo actualizarás tú en el código o vía CSV)
        datos_oficiales = [
            ("🇦🇷 Argentina", 2, "🇫🇷 Francia", 1, True),
            ("🇲🇽 México", 0, "🇺🇸 EE.UU.", 0, True)
        ]
        
        for zona, equipos in mundial.items():
            st.subheader(f"Estado Oficial {zona}")
            res_filtrados = [r for r in datos_oficiales if r[0] in equipos]
            tabla_real_df = calcular_tabla(equipos, res_filtrados)
            st.table(tabla_real_df.style.set_properties(**{'background-color': '#f9f9f9', 'color': '#1a472a', 'font-weight': 'bold'}))
