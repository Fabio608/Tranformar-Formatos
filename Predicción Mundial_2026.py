import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽")

st.markdown("<h1 style='text-align: center;'>⚽ Prode Mundial 2026</h1>", unsafe_allow_html=True)

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_data = conn.read()
except Exception as e:
    # Si falla la conexión, creamos una tabla vacía para que la app no tire error
    df_data = pd.DataFrame(columns=["Usuario", "Puntos", "Aciertos_Exactos"])
    st.sidebar.warning("⚠️ Base de datos no conectada (Modo Prueba)")

# --- 3. LÓGICA DE TIEMPO (Argentina UTC-3) ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)
tiempo_restante = fecha_limite - ahora

# --- 4. MENÚ ---
menu = ["📊 Tabla y Premios", "📝 Cargar Pronósticos", "⚙️ Configuración"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "📊 Tabla y Premios":
    st.header("🏆 Ranking del Grupo")
    
    # Cuadro de Premio
    st.info("🎁 **PREMIO:** Un asado completo para el ganador.")
    
    if not df_data.empty:
        df_ranking = df_data.sort_values(by=["Puntos", "Aciertos_Exactos"], ascending=False).reset_index(drop=True)
        df_ranking.index += 1
        st.table(df_ranking)
    else:
        st.write("Aún no hay puntos cargados.")

    st.markdown("""
    <p style='font-size: 0.8rem; color: gray;'>
    <b>⚖️ Desempate:</b> 1. Marcadores exactos | 2. Ganadores acertados | 3. Fecha de envío.
    </p>
    """, unsafe_allow_html=True)

elif choice == "📝 Cargar Pronósticos":
    st.header("📝 Tus Predicciones")
    
    if ahora > fecha_limite:
        st.error("❌ El plazo terminó el 10 de junio.")
    else:
        st.warning(f"⏳ Tienes tiempo hasta el 10 de junio (Faltan {tiempo_restante.days} días).")
        nombre = st.text_input("Tu Nombre:")
        
        # Ejemplo de Grupos
        mundial = {
            "ZONA J": ["Argentina", "Argelia", "Jordania", "Austria"],
            "ZONA A": ["México", "Sudáfrica", "Corea del Sur", "Rep. Checa"]
        }
        
        for zona, equipos in mundial.items():
            with st.expander(f"⚽ {zona}"):
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        c1, c2, c3 = st.columns([2, 1, 2])
                        with c1: st.write(equipos[i])
                        with c2: st.selectbox("vs", ["-", "Gana L", "Empate", "Gana V"], key=f"{zona}_{i}_{j}")
                        with c3: st.write(equipos[j])

        if st.button("✅ ENVIAR RESULTADOS"):
            if nombre:
                st.success(f"¡{nombre}, recibimos tus datos!")
                st.balloons()
            else:
                st.error("Falta tu nombre.")

# --- COMPARTIR ---
st.sidebar.write("---")
link = "https://tu-app.streamlit.app"
msg = urllib.parse.quote(f"¡Unite al Prode! {link}")
st.sidebar.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank">📲 Invitar Amigos</a>', unsafe_allow_html=True)
