import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA PREMIUM ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="🏆", layout="wide")

st.markdown("""
    <style>
    /* Fondo con overlay oscuro para que el texto resalte más */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1551958219-acbc608c6377?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Contenedor principal estilo 'glassmorphism' */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 50px;
        margin-top: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Nombres de equipos más elegantes */
    .nombre-equipo {
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #1a1a1a !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Ocultar flechas de los inputs */
    button.step-up, button.step-down { display: none !important; }
    
    /* Inputs de goles estilo 'Sport' */
    div[data-testid="stNumberInput"] { width: 60px !important; margin: 0 auto; }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        border: 2px solid #1a472a !important;
        border-radius: 10px !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    input {
        text-align: center !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        color: #1a472a !important;
    }
    
    .guion { font-size: 1.6rem; font-weight: bold; color: #333; margin-top: 2px; }

    /* Títulos con sombra */
    h1 { color: #1a472a; text-align: center; font-weight: 900; font-size: 3.5rem !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    h3 { color: #1a472a; font-weight: 800; border-left: 5px solid #1a472a; padding-left: 15px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>⚽ PRODE MUNDIAL 2026 </h1>", unsafe_allow_html=True)

# --- 2. LÓGICA DE TIEMPO ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)
tiempo_restante = fecha_limite - ahora

# --- 3. DEFINICIÓN DE GRUPOS (Con Banderas) ---
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
    tabla = pd.DataFrame({
        'Equipo': equipos,
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    for res in resultados:
        e1, g1, e2, g2, jugado = res
        if jugado:
            tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
            tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g1 < g2: tabla.loc[e2, 'Pts'] += 3
            else:
                tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    tabla['DG'] = tabla['GF'] - tabla['GC']
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 4. INTERFAZ ---
if ahora > fecha_limite:
    st.error("❌ El plazo de entrega finalizó.")
else:
    st.markdown(f"🗓️ **Fecha límite:** 10 de Junio de 2026 | ⏳ **Faltan:** {tiempo_restante.days} días.")
    nombre = st.text_input("👤 **INGRESÁ TU NOMBRE PARA EMPEZAR:**", placeholder="Ej: Lionel Messi")

    predicciones_para_mensaje = []

    for zona, equipos in mundial.items():
        st.subheader(f"🏆 {zona}")
        col_partidos, col_tabla = st.columns([1.3, 1])
        resultados_grupo = []
        
        with col_partidos:
            st.markdown("<div style='padding-right:20px;'>", unsafe_allow_html=True)
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    c1, c2, c3, c4, c5 = st.columns([2, 0.7, 0.3, 0.7, 2])
                    with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{equipos[i]}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"g1_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c3: st.markdown("<p class='guion'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"g2_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{equipos[j]}</p>", unsafe_allow_html=True)
                    
                    # Lógica de detección de cambio
                    jugado = (g1 > 0 or g2 > 0)
                    resultados_grupo.append((equipos[i], g1, equipos[j], g2, jugado))
                    if jugado: predicciones_para_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_tabla:
            st.markdown("<p style='font-weight: 800; color: #1a472a; margin-bottom: 10px;'>📊 TABLA EN TIEMPO REAL</p>", unsafe_allow_html=True)
            df_tabla = calcular_tabla(equipos, resultados_grupo)
            
            # Estilo avanzado de tabla
            estilo_tabla = df_tabla.style.set_properties(**{
                'background-color': 'white',
                'color': 'black',
                'border-color': '#e0e0e0',
                'text-align': 'center'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#1a472a'), ('color', 'white'), ('font-weight', 'bold')]},
                {'selector': 'tr:hover', 'props': [('background-color', '#f5f5f5')]}
            ]).highlight_max(subset=['Pts'], color='#c8e6c9') # Resalta ganador en verde suave
            
            st.dataframe(estilo_tabla, use_container_width=True)

    # --- 5. BOTÓN FINAL ---
    st.divider()
    col_btn, _ = st.columns([1, 1])
    with col_btn:
        if st.button("🚀 FINALIZAR Y GENERAR MENSAJE"):
            if nombre and predicciones_para_mensaje:
                resumen = f"🏆 PRODE MUNDIAL 2026\n👤 Jugador: {nombre.upper()}\n" + "="*25 + "\n"
                resumen += "\n".join(predicciones_para_mensaje)
                resumen += "\n" + "="*25 + "\n⚽ ¡Copiame y pegame en el grupo!"
                
                st.success("✅ ¡Pronóstico completado!")
                st.code(resumen, language="text")
                st.balloons()
            elif not nombre:
                st.warning("⚠️ Escribí tu nombre para poder finalizar.")
            else:
                st.info("⚠️ Cargá al menos un resultado de partido.")
