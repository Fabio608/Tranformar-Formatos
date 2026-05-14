import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA DE MÁXIMA LEGIBILIDAD ---
st.set_page_config(page_title="Mundial 2026 - Predicción vs Realidad", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    /* Fondo con overlay más oscuro para que resalte el contenedor blanco */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Contenedor Principal Blanco Opaco (Sin transparencias) */
    .main .block-container {
        background-color: #FFFFFF !important; 
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.7);
    }
    
    /* TEXTOS GENERALES (FUERZA NEGRO ABSOLUTO) */
    span, p, label, .stMarkdown {
        color: #000000 !important;
        font-weight: 600;
    }

    /* NOMBRES DE EQUIPOS */
    .nombre-equipo {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: #000000 !important; 
        text-transform: uppercase;
    }

    .guion {
        font-size: 1.8rem;
        font-weight: 900;
        color: #000000 !important;
        text-align: center;
    }

    /* INPUTS DE GOLES */
    button.step-up, button.step-down { display: none !important; }
    div[data-testid="stNumberInput"] { width: 70px !important; margin: 0 auto; }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        border: 3px solid #1a472a !important; /* Borde más grueso */
        border-radius: 8px !important;
        background-color: #F0F2F6 !important;
    }
    input {
        text-align: center !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        color: #1a472a !important; /* Verde oscuro para el número */
    }

    /* TÍTULOS PRINCIPALES */
    h1 { 
        color: #1a472a !important; 
        text-align: center; 
        font-weight: 900; 
        font-size: 3.5rem !important; 
        margin-bottom: 20px;
    }
    
    h2, h3 { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        border-bottom: 2px solid #1a472a;
        padding-bottom: 10px;
    }

    /* ESTILO DE LAS PESTAÑAS */
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #444444 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #1a472a !important;
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
    st.error("❌ El plazo de entrega finalizó el 10 de junio a las 23:59 (Hora Local Argentina).")
else:
    tab_pred, tab_real = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES"])

    with tab_pred:
        st.markdown(f"🗓️ **LÍMITE:** 10/06/2026 23:59hs | ⏳ **FALTAN:** {tiempo_restante.days} días y {tiempo_restante.seconds//3600} horas.")
        nombre = st.text_input("👤 **ESCRIBE TU NOMBRE AQUÍ:**", placeholder="Tu nombre...")
        
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
                        with c2: g1 = st.number_input("", 0, 20, 0, key=f"v_{zona}_{i}_{j}", label_visibility="collapsed")
                        with c3: st.markdown("<p class='guion'>-</p>", unsafe_allow_html=True)
                        with c4: g2 = st.number_input("", 0, 20, 0, key=f"v2_{zona}_{i}_{j}", label_visibility="collapsed")
                        with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{equipos[j]}</p>", unsafe_allow_html=True)
                        
                        jugado = (g1 > 0 or g2 > 0)
                        res_usuario.append((equipos[i], g1, equipos[j], g2, jugado))
                        if jugado: predicciones_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
            
            with col_tabla:
                st.markdown("<p style='color:#000; font-weight:bold;'>📊 TU POSICIONES:</p>", unsafe_allow_html=True)
                tabla_est = calcular_tabla(equipos, res_usuario)
                st.dataframe(tabla_est.style.set_properties(**{'color': 'black', 'font-weight': 'bold'}), use_container_width=True)

        st.divider()
        if st.button("✅ Finalizar y Compartir"):
            if nombre and predicciones_mensaje:
                resumen = f"🏆 PREDICCIÓN MUNDIAL 2026\n👤 JUGADOR: {nombre.upper()}\n" + "="*25 + "\n"
                resumen += "\n".join(predicciones_mensaje)
                st.success("✅ ¡Pronóstico generado! Copia el texto:")
                st.code(resumen, language="text")
                st.balloons()
            else:
                st.warning("⚠️ Por favor, ingresa tu nombre y al menos un marcador.")

    with tab_real:
        st.header("🏁 Resultados Oficiales")
        st.write("Consulta aquí el avance real del torneo.")
        
        # Datos de ejemplo (se actualizan manualmente en el código)
        datos_oficiales = [
            ("🇦🇷 Argentina", 1, "🇫🇷 Francia", 0, True)
        ]
        
        for zona, equipos in mundial.items():
            st.subheader(f"Estado Oficial {zona}")
            res_filtrados = [r for r in datos_oficiales if r[0] in equipos]
            tabla_real_df = calcular_tabla(equipos, res_filtrados)
            st.table(tabla_real_df.style.set_properties(**{'background-color': '#f0f0f0', 'color': 'black', 'font-weight': 'bold'}))
