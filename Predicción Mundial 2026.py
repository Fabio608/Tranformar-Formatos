import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# --- 1. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽")

# Título Principal
st.markdown("<h1 style='text-align: center;'>⚽ Prode Mundial 2026</h1>", unsafe_allow_html=True)

# --- 2. BASE DE DATOS (CONEXIÓN GOOGLE SHEETS) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_data = conn.read()
except:
    st.error("⚠️ Error de conexión. Asegúrate de configurar los 'Secrets' en Streamlit Cloud.")
    df_data = pd.DataFrame(columns=["Usuario", "Puntos", "Aciertos_Exactos"])

# --- 3. LÓGICA DE FECHA LÍMITE ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)
tiempo_restante = fecha_limite - ahora

# --- 4. MENÚ LATERAL (SIDEBAR) ---
st.sidebar.header("Menú del Torneo")
menu = ["📊 Tabla y Premios", "📝 Cargar Pronósticos", "⚙️ Configuración Grupo"]
choice = st.sidebar.selectbox("Ir a:", menu)

# --- SECCIÓN: CONFIGURACIÓN (ADMIN) ---
if choice == "⚙️ Configuración Grupo":
    st.header("⚙️ Configuración del Grupo")
    nombre_grupo = st.text_input("Nombre del Grupo de WhatsApp:", value="Los Pibes de Comodoro")
    premio_actual = st.text_area("Premio para el Ganador:", "Ej: Un asado y un Fernet")
    
    if st.button("Guardar Cambios"):
        st.success("Configuración actualizada para todos los integrantes.")

# --- SECCIÓN: TABLA Y PREMIOS ---
elif choice == "📊 Tabla y Premios":
    st.header("🏆 Posiciones y Premios")
    
    # Cuadro de Premio (Editable por el Admin)
    st.info(f"🎁 **PREMIO ACTUAL:** {st.session_state.get('premio', 'Un asado para el primer puesto')}")
    
    # Ranking
    st.subheader("Ranking del Grupo")
    if not df_data.empty:
        # Lógica de orden: 1° Puntos, 2° Aciertos Exactos
        df_ranking = df_data.sort_values(by=["Puntos", "Aciertos_Exactos"], ascending=False).reset_index(drop=True)
        df_ranking.index += 1
        st.table(df_ranking)
    else:
        st.write("Aún no hay resultados cargados.")

    # Letra Chica (Desempate)
    st.markdown("""
    ---
    <p style='font-size: 0.8rem; color: gray;'>
    <b>⚖️ Método de Desempate (Letra Chica):</b><br>
    En caso de igualdad de puntos, el orden se definirá por: <br>
    1. Mayor cantidad de resultados exactos acertados.<br>
    2. Mayor cantidad de ganadores acertados (sin marcador exacto).<br>
    3. Fecha de carga del pronóstico (el que cargó primero gana).
    </p>
    """, unsafe_allow_html=True)

# --- SECCIÓN: CARGAR PRONÓSTICOS ---
elif choice == "📝 Cargar Pronósticos":
    st.header("📝 Tus Predicciones")
    
    if ahora > fecha_limite:
        st.error(f"❌ El plazo expiró el {fecha_limite.strftime('%d/%m/%Y %H:%M')}. Ya no se aceptan cambios.")
    else:
        st.warning(f"⏳ Tienes hasta el 10 de junio a las 23:59 para enviar (Faltan: {tiempo_restante.days} días).")
        
        nombre_usuario = st.text_input("Tu Nombre/Apodo:")
        
        # Listado de Grupos del Mundial
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
        
        for grupo, equipos in mundial.items():
            with st.expander(f"⚽ {grupo}"):
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        col1, col2, col3 = st.columns([2, 1, 2])
                        with col1: st.write(equipos[i])
                        with col2: res = st.selectbox("vs", ["-", "Gana L", "Empate", "Gana V"], key=f"{grupo}_{i}_{j}")
                        with col3: st.write(equipos[j])

        if st.button("✅ AFIRMAR Y ENTREGAR RESULTADOS"):
            if not nombre_usuario:
                st.error("Por favor, ingresa tu nombre.")
            else:
                st.success(f"¡{nombre_usuario}, tus resultados se enviaron correctamente!")
                st.balloons()

# --- BOTÓN WHATSAPP EN EL PIE ---
st.sidebar.write("---")
link_app = "https://tu-prode.streamlit.app"
msg = f"¡Unite al Prode del Mundial! Entrá acá para cargar tus resultados: {link_app}"
url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
st.sidebar.markdown(f'<a href="{url_wa}" target="_blank">📲 Invitar Amigos por WhatsApp</a>', unsafe_allow_html=True)
