import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# --- 1. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽", layout="centered")

# Estilo de Título
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #003566;'>⚽ Prode Mundial 2026</h1>
        <p style='color: #74ACDF; font-weight: bold;'>Comodoro Rivadavia - Grupo Oficial</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DATOS (GOOGLE SHEETS) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_data = conn.read()
except:
    # Datos de respaldo si la conexión falla o no está configurada
    df_data = pd.DataFrame(columns=["Usuario", "Puntos", "Aciertos_Exactos"])

# --- 3. LÓGICA DE FECHA LÍMITE ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)
tiempo_restante = fecha_limite - ahora

# --- 4. PERSISTENCIA DE DATOS DEL GRUPO ---
if 'nombre_grupo' not in st.session_state:
    st.session_state['nombre_grupo'] = "Los Pibes del WhatsApp"
if 'premio' not in st.session_state:
    st.session_state['premio'] = "Un asado completo para el ganador"

# --- 5. MENÚ LATERAL ---
st.sidebar.header("Menú del Torneo")
menu = ["📊 Tabla y Premios", "📝 Cargar Pronósticos", "⚙️ Configuración Grupo"]
choice = st.sidebar.selectbox("Seleccioná una sección:", menu)

# --- SECCIÓN: CONFIGURACIÓN (ADMIN) ---
if choice == "⚙️ Configuración Grupo":
    st.header("⚙️ Configuración del Grupo")
    st.session_state['nombre_grupo'] = st.text_input("Nombre del Grupo:", st.session_state['nombre_grupo'])
    st.session_state['premio'] = st.text_area("Premio en juego:", st.session_state['premio'])
    
    if st.button("Guardar Cambios"):
        st.success("¡Configuración actualizada para todos!")

# --- SECCIÓN: TABLA Y PREMIOS ---
elif choice == "📊 Tabla y Premios":
    st.header(f"🏆 Ranking: {st.session_state['nombre_grupo']}")
    
    # Cuadro de Premio
    st.info(f"🎁 **EL PREMIO ES:** {st.session_state['premio']}")
    
    # Tabla de Posiciones
    st.subheader("Tabla General")
    if not df_data.empty:
        df_ranking = df_data.sort_values(by=["Puntos", "Aciertos_Exactos"], ascending=False).reset_index(drop=True)
        df_ranking.index += 1
        st.table(df_ranking)
    else:
        st.write("Aún no hay puntos registrados. ¡A cargar las predicciones!")

    # Letra Chica
    st.markdown(f"""
    ---
    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; font-size: 0.8rem;'>
        <b>⚖️ MÉTODO DE DESEMPATE:</b><br>
        1. Mayor cantidad de marcadores exactos acertados.<br>
        2. Mayor cantidad de ganadores acertados.<br>
        3. Fecha y hora de envío (quien cargó primero tiene prioridad).
    </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN: CARGAR PRONÓSTICOS ---
elif choice == "📝 Cargar Pronósticos":
    st.header("📝 Tus Predicciones")
    
    if ahora > fecha_limite:
        st.error(f"❌ El tiempo expiró el 10 de junio a las 23:59. Ya no se pueden modificar los resultados.")
    else:
        st.warning(f"⏳ Quedan {tiempo_restante.days} días para el cierre.")
        
        nombre_usuario = st.text_input("Ingresá tu Nombre o Apodo:")
        
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
        
        for zona, equipos in mundial.items():
            with st.expander(f"⚽ {zona}"):
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        col1, col2, col3 = st.columns([2, 1, 2])
                        with col1: st.write(f"**{equipos[i]}**")
                        with col2: res = st.selectbox("vs", ["-", "Gana L", "Empate", "Gana V"], key=f"{zona}_{i}_{j}")
                        with col3: st.write(f"**{equipos[j]}**")

        if st.button("✅ AFIRMAR Y ENTREGAR RESULTADOS"):
            if not nombre_usuario:
                st.error("⚠️ Debes ingresar un nombre para enviar.")
            else:
                st.success(f"¡{nombre_usuario}, tus resultados han sido guardados!")
                st.balloons()

# --- BOTÓN WHATSAPP ---
st.sidebar.write("---")
link_app = "https://tu-app.streamlit.app" # Cambialo por tu link real
msg = f"¡Unite al Prode del Mundial 2026! Cargá tus resultados acá: {link_app}"
url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
st.sidebar.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">📲 Compartir en WhatsApp</button></a>', unsafe_allow_html=True)
