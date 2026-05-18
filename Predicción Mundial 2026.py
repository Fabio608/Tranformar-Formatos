import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import urllib.parse  # Para codificar el mensaje de WhatsApp de forma segura

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Pronosticador Mundial 2026", page_icon="🏆", layout="wide")

AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 11, 0, 0, 0, tzinfo=AR)
ahora = datetime.now(AR)

# Mapeo de banderas oficiales para cada selección participante (sin abreviaciones)
banderas = {
    "GRUPO A": ["México", "Sudáfrica", "Corea del Sur", "República Checa"],
    "GRUPO B": ["Canadá", "Bosnia y Herzegovina", "Qatar", "Suiza"],
    "GRUPO C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "GRUPO D": ["Estados Unidos", "Australia", "Paraguay", "Turquía"],
    "GRUPO E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "GRUPO F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "GRUPO G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
    "GRUPO H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
    "GRUPO I": ["Francia", "Senegal", "Irak", "Noruega"],
    "GRUPO J": ["Argentina", "Argelia", "Jordania", "Austria"],
    "GRUPO K": ["Portugal", "República Democrática del Congo", "Uzbekistán", "Colombia"],
    "GRUPO L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;700;900&display=swap');

    /* Fondo del Estadio de Noche */
    .stApp {
        background: linear-gradient(rgba(10, 15, 30, 0.92), rgba(6, 10, 20, 0.95)),
                    url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Título Oficial */
    .titulo-personalizado {
        font-family: 'Archivo Black', sans-serif;
        background: linear-gradient(135deg, #FFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        text-align: center;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
        filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.5));
    }

    .subtitulo-personalizado {
        font-family: 'Inter', sans-serif;
        color: #00FFCC;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Banner de cuenta regresiva */
    .countdown-banner {
        background: linear-gradient(90deg, rgba(255,140,0,0.15) 0%, rgba(0,255,204,0.1) 100%);
        border: 1px solid rgba(0,255,204,0.3);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,255,204,0.1);
    }

    /* Título de Grupos de la Copa */
    .titulo-zona {
        font-family: 'Archivo Black', sans-serif;
        color: #FF8C00 !important;
        font-size: 1.6rem !important;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 3px solid #FF8C00;
        width: fit-content;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .nombre-equipo {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }

    /* --- ESTILO DE LA TABLA DE CLASIFICACIÓN --- */
    [data-testid="stTable"] {
        background-color: rgba(10, 15, 30, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="stTable"] thead th {
        background-color: rgba(255, 140, 0, 0.15) !important;
        color: #FFD700 !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
    }

    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        text-align: center !important;
        padding: 12px 10px !important;
    }
    [data-testid="stTable"] td:last-child, [data-testid="stTable"] th:last-child { border-right: none !important; }

    /* Indicadores visuales de clasificación (Verde 1°, Azul 2°) */
    [data-testid="stTable"] tr:nth-child(1) td {
        background-color: rgba(46, 204, 113, 0.12) !important; /* Clasificado 1 */
        border-left: 4px solid #2ecc71 !important;
    }
    [data-testid="stTable"] tr:nth-child(2) td {
        background-color: rgba(52, 152, 219, 0.08) !important; /* Clasificado 2 */
        border-left: 4px solid #3498db !important;
    }

    /* --- CONTROLES DE RESULTADOS ESTILO SCOREBOARD --- */

    /* Quitar flechas de número por completo */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none !important;
      margin: 0 !important;
    }
    input[type=number] {
      -moz-appearance: textfield !important;
    }

    /* Ocultar la cruz "X" (clear button) de Streamlit */
    [data-testid="stInputClearButton"],
    button[aria-label="Clear input"],
    div[data-baseweb="input"] svg,
    div[data-testid="stNumberInput"] button {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Caja contenedora: Color blanco/gris claro para máxima legibilidad */
    div[data-baseweb="input"] {
        background-color: #F5F5F7 !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 10px rgba(255,140,0,0.15) !important;
        transition: all 0.3s ease !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #00FFCC !important;
        box-shadow: 0 0 10px rgba(0,255,204,0.5) !important;
    }

    /* El número ingresado: Grande, centrado y NEGRO INTENSO */
    div[data-testid="stNumberInput"] input {
        background-color: transparent !important;
        color: #000000 !important;
        font-family: 'Archivo Black', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        padding: 4px !important;
        border: none !important;
    }

    /* Estilo para los selectores de Solapas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255,255,255,0.03) !important;
        padding: 8px !important;
        border-radius: 12px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: rgba(255,255,255,0.6) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF8C00 !important;
        color: #000000 !important;
        box-shadow: 0 4px 15px rgba(255,140,0,0.3) !important;
    }
    </style>

    <div style="text-align: center; padding: 15px 0;">
        <span class="titulo-personalizado">FIFA WORLD CUP 2026</span>
        <div class="subtitulo-personalizado">PRONOSTICADOR DE GRUPOS </div>
    </div>
    """, unsafe_allow_html=True)

# # STREAMING_CHUNK: Calculando días restantes para el inicio del Mundial...
dias_restantes = (fecha_limite - ahora).days
if dias_restantes > 0:
    st.markdown(f"""
        <div class="countdown-banner">
            ⚽ ¡FALTAN SÓLO 🏟️ <span style="color:#00FFCC; font-size: 1.3rem;">{dias_restantes} DÍAS</span> PARA EL PARTIDO INAUGURAL DE LA COPA DEL MUNDO!
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="countdown-banner" style="border-color: #2ecc71;">
            🔥🏆 ¡EL MUNDIAL DE LA FIFA 2026 YA ESTÁ EN JUEGO! ¡QUE GANEN LOS MEJORES! ⚽
        </div>
    """, unsafe_allow_html=True)

# Grupos oficiales del Mundial de 48 equipos (sin abreviaciones)
mundial = {
    "GRUPO A": ["México", "Sudáfrica", "Corea del Sur", "República Checa"],
    "GRUPO B": ["Canadá", "Bosnia y Herzegovina", "Qatar", "Suiza"],
    "GRUPO C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "GRUPO D": ["Estados Unidos", "Australia", "Paraguay", "Turquía"],
    "GRUPO E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "GRUPO F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "GRUPO G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
    "GRUPO H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
    "GRUPO I": ["Francia", "Senegal", "Irak", "Noruega"],
    "GRUPO J": ["Argentina", "Argelia", "Jordania", "Austria"],
    "GRUPO K": ["Portugal", "República Democrática del Congo", "Uzbekistán", "Colombia"],
    "GRUPO L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
}

# # STREAMING_CHUNK: Definiendo la lógica para calcular las tablas de posiciones...
def calcular_df(equipos, resultados_dict):
    tabla = pd.DataFrame(0, index=equipos, columns=['Pts', 'PJ', 'GF', 'GC', 'DG'])
    tabla.index.name = "Equipos"
    equipos_set = set(equipos)

    for (e1, e2), (g1, g2) in resultados_dict.items():
        # Procesar solo si ambos equipos pertenecen a este grupo actual
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

# # STREAMING_CHUNK: Agregando función para armar el mensaje de WhatsApp...
def generar_url_whatsapp(nombre, dict_p):
    texto = "🏆 *Mi Pronóstico de Grupos - Mundial 2026* ⚽\n"
    if nombre:
        texto += f"👤 *Pronosticador:* {nombre}\n\n"
    else:
        texto += f"👤 *Mis Clasificados:*

"

    for grupo, equipos in mundial.items():
        df_ordenado = calcular_df(equipos, dict_p)
        clasificado_1 = df_ordenado.index[0]
        clasificado_2 = df_ordenado.index[1]

        b1 = banderas.get(clasificado_1, "")
        b2 = banderas.get(clasificado_2, "")

        texto += f"🔸 *{grupo}:* 1° {b1} {clasificado_1} | 2° {b2} {clasificado_2}\n"

    texto += "\n🔮 _¿Y vos? ¡Armá tu pronóstico aquí!_"
    texto_codificado = urllib.parse.quote(texto)
    return f"https://wa.me/?text={texto_codificado}"

# --- 3. INTERFAZ EN TABS ---
tab_p, tab_r, tab_c = st.tabs(["🔮 MI PRONÓSTICO", "📈 RESULTADOS REALES", "🎯 PUNTAJE FINAL"])

# # STREAMING_CHUNK: Creando la interfaz de la pestaña 'MI PRONÓSTICO' con banderas en partidos...
with tab_p:
    puede_p = ahora < fecha_limite
    st.markdown("<p style='color: white;'>📅 Se puede editar hasta el 10 de Junio de 2026 inclusive.</p>", unsafe_allow_html=True)

    # Capturamos el nombre
    st.markdown("<p class='nombre-equipo'>👤 **INGRESÁ TU NOMBRE DE PRONOSTICADOR:**</p>", unsafe_allow_html=True)
    user_name = st.text_input("", key="user_name", placeholder="Ej: Juan Pérez", label_visibility="collapsed")

    dict_p = {}
    for grupo, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚽ {grupo}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])

        with c1:
            # Lista de partidos cara a cara con emojis de banderas sumados
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]

                    b1 = banderas.get(e1, "")
                    b2 = banderas.get(e2, "")

                    cols = st.columns([2.2, 0.7, 0.2, 0.7, 2.2])

                    cols[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{b1} {e1}</p>", unsafe_allow_html=True)
                    v1 = cols[1].number_input("", 0, 20, value=None, key=f"p1_{e1}_{e2}_{grupo}", label_visibility="collapsed", disabled=not puede_p)
                    cols[2].markdown("<p style='text-align:center; color:white; font-weight:bold;'>-</p>", unsafe_allow_html=True)
                    v2 = cols[3].number_input("", 0, 20, value=None, key=f"p2_{e1}_{e2}_{grupo}", label_visibility="collapsed", disabled=not puede_p)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{b2} {e2}</p>", unsafe_allow_html=True)

                    dict_p[(e1, e2)] = (v1, v2)

        with c2:
            df_tabla = calcular_df(equipos, dict_p)
            df_vista = df_tabla.copy()
            # Mapear índice con banderas
            df_vista.index = [f"{banderas.get(team, '')} {team}" for team in df_vista.index]
            # Resetear índice para que "Equipos" sea una columna visible en el encabezado
            df_vista = df_vista.reset_index().rename(columns={"index": "Equipos"})
            st.table(df_vista)

    # Sección de acciones finales
    st.markdown("---")
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        st.button("✅ Guardar Pronóstico", disabled=not puede_p, use_container_width=True)
    with col_btn2:
        url_wa = generar_url_whatsapp(user_name, dict_p)
        st.link_button("📲 Compartir mi Pronóstico por WhatsApp", url_wa, type="primary", use_container_width=True)

# # STREAMING_CHUNK: Configurando la pestaña 'RESULTADOS REALES' con el ícono de pelota de fútbol...
with tab_r:
    puede_r = ahora >= fecha_limite
    if not puede_r:
        st.warning("🔒 Los resultados reales se habilitarán automáticamente el 11 de Junio una vez iniciado el evento.")

    dict_r = {}
    for grupo, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚽ {grupo}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])

        with c1:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    e1, e2 = equipos[i], equipos[j]
                    b1 = banderas.get(e1, "")
                    b2 = banderas.get(e2, "")

                    cols = st.columns([2.2, 0.7, 0.2, 0.7, 2.2])
                    cols[0].markdown(f"<p class='nombre-equipo' style='text-align:right;'>{b1} {e1}</p>", unsafe_allow_html=True)
                    v1 = cols[1].number_input("", 0, 20, value=None, key=f"r1_{e1}_{e2}_{grupo}", label_visibility="collapsed", disabled=not puede_r)
                    cols[2].write("-")
                    v2 = cols[3].number_input("", 0, 20, value=None, key=f"r2_{e1}_{e2}_{grupo}", label_visibility="collapsed", disabled=not puede_r)
                    cols[4].markdown(f"<p class='nombre-equipo' style='text-align:left;'>{b2} {e2}</p>", unsafe_allow_html=True)

                    dict_r[(e1, e2)] = (v1, v2)

        with c2:
            df_tabla_r = calcular_df(equipos, dict_r)
            df_vista_r = df_tabla_r.copy()
            df_vista_r.index = [f"{banderas.get(team, '')} {team}" for team in df_vista_r.index]
            df_vista_r = df_vista_r.reset_index().rename(columns={"index": "Equipos"})
            st.table(df_vista_r)

# # STREAMING_CHUNK: Diseñando el panel de 'PUNTAJE FINAL' con banderas...
with tab_c:
    puntos_totales = 0
    for grupo, equipos in mundial.items():
        st.markdown(f"<div class='titulo-zona'>⚖️ Comparación {grupo}</div>", unsafe_allow_html=True)
        orden_p = calcular_df(equipos, dict_p).index.tolist()
        orden_r = calcular_df(equipos, dict_r).index.tolist()

        ca, cb, cc = st.columns(3)
        for idx in range(4):
            # Solo puntuamos si se cargó al menos algún resultado real
            if any(v is not None for v in sum(dict_r.values(), ())):
                p = 2 if orden_p[idx] == orden_r[idx] else (1 if orden_p[idx] in orden_r[:2] and orden_r[idx] in orden_p[:2] else 0)
            else:
                p = 0

            puntos_totales += p

            p_flag = banderas.get(orden_p[idx], "")
            r_flag = banderas.get(orden_r[idx], "")

            ca.markdown(f"<span class='nombre-equipo'>🔮 {idx+1}° {p_flag} {orden_p[idx]}</span>", unsafe_allow_html=True)
            cb.markdown(f"<span class='nombre-equipo'>🏟️ Real: {r_flag} {orden_r[idx]}</span>", unsafe_allow_html=True)
            cc.write(f"⭐ +{p} pts")

    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FF8C00, #FFD700); padding:20px; border-radius:14px; text-align:center; box-shadow: 0 4px 20px rgba(255,140,0,0.3);'>
            <h2 style='color:black; font-family: "Archivo Black", sans-serif; margin:0;'>MI MARCADOR TOTAL: {puntos_totales} PUNTOS</h2>
        </div>
    """, unsafe_allow_html=True)
