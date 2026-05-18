import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import urllib.parse  # Para codificar el mensaje de WhatsApp de forma segura

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Predicción Mundial 2026", page_icon="⚽", layout="wide")

AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
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

    .titulo-personalizado {
        font-family: 'Archivo Black', sans-serif;
        color: black;
        font-size: 2.8rem !important;
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

    /* --- ESTILO DE TABLA --- */
    [data-testid="stTable"] { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        border-radius: 15px !important; 
        border: 1px solid rgba(255, 140, 0, 0.5) !important; 
        overflow: hidden !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th { 
        color: white !important; 
        font-family: 'Inter', sans-serif !important; 
        border-bottom: 1px solid rgba(255, 140, 0, 0.3) !important; 
        border-right: 1px solid rgba(255, 140, 0, 0.3) !important; 
        text-align: center !important; 
        padding: 10px !important; 
    }
    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child { border-right: none !important; }

    /* --- CORRECCIÓN DE INPUTS (COLOR NEGRO Y SIN CRUCES) --- */
    
    /* Quita las flechas de número (spinners) */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none !important;
      margin: 0 !important;
    }
    input[type=number] {
      -moz-appearance: textfield !important;
    }

    /* Oculta de manera agresiva botones de borrar y cruz interna de Streamlit */
    [data-testid="stInputClearButton"], 
    button[aria-label="Clear input"],
    div[data-baseweb="input"] svg,
    div[data-testid="stNumberInput"] button {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Contenedor principal del input: fondo gris claro para que contraste el número negro */
    div[data-baseweb="input"] {
        background-color: #f0f0f0 !important; 
        border: 2px solid #FF8C00 !important; 
        border-radius: 6px !important;
    }

    /* El input numérico: Texto completamente negro y súper legible */
    div[data-testid="stNumberInput"] input { 
        background-color: transparent !important; 
        color: black !important; 
        font-weight: 900 !important; 
        text-align: center !important;
        padding: 5px !important;
        border: none !important;
    }

    /* Efecto al seleccionar el input */
    div[data-baseweb="input"]:focus-within {
        border-color: white !important;
    }
    </style>
    
    <div style="text-align: center; padding: 15px 0;">
        <span class="titulo-personalizado">Predicción Mundial 2026</span>
    </div>
    """, unsafe_allow_html=True)

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

def calcular_df(equipos, resultados_dict):
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "Equipos"
    equipos_set = set(equipos)
    for (e1, e2), (g1, g2) in resultados_dict.items():
        # Procesamos solo los equipos correspondientes a la zona evaluada para evitar KeyError
        if e1 in equipos_set and e2 in equipos_set:
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

def generar_url_whatsapp(nombre, dict_p):
    texto = "🏆 *Mi Predicción para el Mundial 2026* ⚽\n"
    if nombre:
        texto += f"👤 *Pronosticador:* {nombre}\n\n"
    else:
        texto += f"👤 *Mi pronóstico de Grupos:*\n\n"
    
    # Recorremos cada zona para extraer el 1° y 2° lugar de la predicción del usuario
    for zona, equipos in mundial.items():
        df_ordenado = calcular_df(equipos, dict_p)
        clasificado_1 = df_ordenado.index[0]
        clasificado_2 = df_ordenado.index[1]
        texto += f"🔸 *{zona}:* 1° {clasificado_1} | 2° {clasificado_2}\n"
        
    texto += "\n🔮 _¿Y vos? ¡Armá tu predicción también!_"
    
    # Codificamos el texto para que sea compatible con una URL de WhatsApp web/móvil
    texto_codificado = urllib.parse.quote(texto)
    return f"https://wa.me/?text={texto_codificado}"

# --- 3. INTERFAZ EN TABS ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PREDICCIÓN", "📈 RESULTADOS REALES", "🎯 PUNTAJE FINAL"])

with tab_p:
    puede_p = ahora < fecha_limite
    st.info("📅 Se puede editar hasta el 10 de Junio de 2026 inclusive.")
    
    # Capturamos el nombre en el session_state para poder usarlo dinámicamente
    user_name = st.text_input("👤 **NOMBRE:**", key="user_name")
    
    dict_p = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.7, 0.2, 0.7, 2])
                    cols[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    v1 = cols[1].number_input("", 0, 20, value=None, key=f"p1_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_p)
                    cols[2].markdown("<p style='text-align:center; color:white;'>•</p>", unsafe_allow_html=True)
                    v2 = cols[3].number_input("", 0, 20, value=None, key=f"p2_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_p)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    dict_p[(e1, e2)] = (v1, v2)
        with c2:
            st.table(calcular_df(equipos, dict_p))
    
    # Fila de acciones al final de la pestaña
    st.markdown("---")
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        st.button("✅ Finalizar Resultados", disabled=not puede_p, use_container_width=True)
    with col_btn2:
        # Generamos dinámicamente la URL con los datos actuales ingresados
        url_wa = generar_url_whatsapp(user_name, dict_p)
        st.link_button("📲 Compartir mi predicción por WhatsApp", url_wa, type="primary", use_container_width=True)

with tab_r:
    puede_r = ahora >= fecha_limite
    if not puede_r:
        st.warning("🔒 Los resultados reales se habilitarán el 11 de Junio.")
    
    dict_r = {}
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>📍 {zona}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    cols = st.columns([2, 0.7, 0.2, 0.7, 2])
                    cols[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{e1}</p>", unsafe_allow_html=True)
                    v1 = cols[1].number_input("", 0, 20, value=None, key=f"r1_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_r)
                    cols[2].write("•")
                    v2 = cols[3].number_input("", 0, 20, value=None, key=f"r2_{e1}_{e2}_{zona}", label_visibility="collapsed", disabled=not puede_r)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{e2}</p>", unsafe_allow_html=True)
                    dict_r[(e1, e2)] = (v1, v2)
        with c2:
            st.table(calcular_df(equipos, dict_r))

with tab_c:
    puntos_totales = 0
    for zona, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ {zona}</div>", unsafe_allow_html=True)
        orden_p = calcular_df(equipos, dict_p).index.tolist()
        orden_r = calcular_df(equipos, dict_r).index.tolist()
        ca, cb, cc = st.columns(3)
        for idx in range(4):
            if any(v is not None for v in sum(dict_r.values(), ())):
                p = 2 if orden_p[idx] == orden_r[idx] else (1 if orden_p[idx] in orden_r[:2] and orden_r[idx] in orden_p[:2] else 0)
            else: p = 0
            puntos_totales += p
            ca.write(f"{idx+1}° {orden_p[idx]}")
            cb.write(f"Real: {orden_r[idx]}")
            cc.write(f"+{p} pts")
    st.markdown(f"<div style='background:#FF8C00; padding:20px; border-radius:10px; text-align:center;'><h2 style='color:black;'>TOTAL: {puntos_totales} PUNTOS</h2></div>", unsafe_allow_html=True)
