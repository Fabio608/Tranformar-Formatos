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
    # Intentamos leer la hoja "Resultados" (asegúrate de que exista en tu Excel)
    df_data = conn.read(worksheet="Resultados")
except Exception as e:
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
    st.info("🎁 **PREMIO:** Un asado completo para el ganador.")
    
    if not df_data.empty:
        # Ordenamos por puntos y luego por aciertos exactos
        df_ranking = df_data.sort_values(by=["Puntos", "Aciertos_Exactos"], ascending=False).reset_index(drop=True)
        df_ranking.index += 1
        st.table(df_ranking)
    else:
        st.write("Aún no hay puntos cargados.")

    st.markdown("<p style='font-size: 0.8rem; color: gray;'><b>⚖️ Desempate:</b> 1. Marcadores exactos | 2. Ganadores acertados | 3. Fecha de envío.</p>", unsafe_allow_html=True)

elif choice == "📝 Cargar Pronósticos":
    st.header("📝 Tus Predicciones")
    
    if ahora > fecha_limite:
        st.error("❌ El plazo terminó el 10 de junio.")
    else:
        st.warning(f"⏳ Tienes tiempo hasta el 10 de junio (Faltan {tiempo_restante.days} días).")
        nombre = st.text_input("Tu Nombre:")
        
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
        
        # Diccionario para capturar las predicciones
        predicciones = {}

        for zona, equipos in mundial.items():
            with st.expander(f"⚽ {zona}"):
                for i in range(len(equipos)):
                    for j in range(i + 1, len(equipos)):
                        c1, c2, c3 = st.columns([2, 1, 2])
                        with c1: st.write(equipos[i])
                        with c2: 
                            resultado = st.selectbox("vs", ["-", "Gana L", "Empate", "Gana V"], key=f"{zona}_{i}_{j}")
                            predicciones[f"{equipos[i]} vs {equipos[j]}"] = resultado
                        with c3: st.write(equipos[j])

        if st.button("✅ ENVIAR RESULTADOS"):
            if nombre and not any(v == "-" for v in predicciones.values()):
                try:
                    # Creamos un DataFrame con el nombre y sus predicciones
                    nueva_entrada = {"Usuario": nombre, "Puntos": 0, "Aciertos_Exactos": 0}
                    nueva_entrada.update(predicciones)
                    
                    df_nuevo = pd.DataFrame([nueva_entrada])
                    
                    # Combinamos con los datos existentes
                    df_actualizado = pd.concat([df_data, df_nuevo], ignore_index=True)
                    
                    # Guardamos en Google Sheets
                    conn.update(worksheet="Resultados", data=df_actualizado)
                    
                    st.success(f"¡{nombre}, tus predicciones han sido guardadas!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            elif not nombre:
                st.error("Por favor, ingresa tu nombre.")
            else:
                st.error("Por favor, completa todos los partidos.")

# --- COMPARTIR ---
st.sidebar.write("---")
link = "https://tu-app.streamlit.app"
msg = urllib.parse.quote(f"¡Unite al Prode! {link}")
st.sidebar.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank">📲 Invitar Amigos</a>', unsafe_allow_html=True)
