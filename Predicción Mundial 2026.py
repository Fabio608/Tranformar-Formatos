import pandas as pd
import urllib.parse

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode WhatsApp", page_icon="🏆")

# --- CONEXIÓN A BASE DE DATOS (OPCIONAL PERO RECOMENDADA) ---
# Si no conectas una base de datos, usará la memoria temporal (se borra al reiniciar)
if "db_participantes" not in st.session_state:
    st.session_state.db_participantes = []
if "db_resultados" not in st.session_state:
    st.session_state.db_resultados = []

# --- INTERFAZ ---
st.title("🏆 Prode del Grupo")

menu = ["🏠 Inicio", "👥 Gestionar Grupo", "⚽ Cargar Resultados", "📊 Tabla de Posiciones"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "🏠 Inicio":
    st.write("### ¡Bienvenido al simulador de posiciones!")
    st.write("Usa el menú lateral para configurar a los 20 integrantes y cargar los puntos.")
    st.image("https://img.freepik.com/vector-premium/campo-futbol-balon-centro_253014-411.jpg")

elif choice == "👥 Gestionar Grupo":
    st.header("Integrantes (Máx 20)")
    nuevo_usuario = st.text_input("Nombre del amigo:")
    if st.button("Agregar"):
        if len(st.session_state.db_participantes) < 20:
            st.session_state.db_participantes.append({"Nombre": nuevo_usuario, "Puntos": 0})
            st.success(f"{nuevo_usuario} se unió al grupo.")
        else:
            st.error("Grupo lleno.")
    
    st.write(pd.DataFrame(st.session_state.db_participantes))

elif choice == "⚽ Cargar Resultados":
    st.header("Cargar Jornada")
    if not st.session_state.db_participantes:
        st.warning("No hay integrantes en el grupo.")
    else:
        with st.form("form_puntos"):
            st.write("Seleccioná quiénes sumaron puntos hoy:")
            ganadores = st.multiselect("¿Quiénes acertaron?", 
                                       [p["Nombre"] for p in st.session_state.db_participantes])
            puntos_a_sumar = st.number_input("Puntos a otorgar:", min_value=1, value=3)
            
            if st.form_submit_button("Repartir Puntos"):
                for p in st.session_state.db_participantes:
                    if p["Nombre"] in ganadores:
                        p["Nombre"] = p["Nombre"] # Mantener nombre
                        p["Puntos"] += puntos_a_sumar
                st.success("¡Puntos actualizados!")

elif choice == "📊 Tabla de Posiciones":
    st.header("Posiciones Actuales")
    if st.session_state.db_participantes:
        df = pd.DataFrame(st.session_state.db_participantes)
        df = df.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
        df.index += 1
        st.table(df)
        
        # Botón WhatsApp
        texto_wa = "🏆 *TABLA DEL GRUPO* 🏆\n\n"
        for i, r in df.iterrows():
            texto_wa += f"{i}. {r['Nombre']}: {r['Puntos']} pts\n"
        
        link = f"https://wa.me/?text={urllib.parse.quote(texto_wa)}"
        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">📲 Compartir en WhatsApp</button></a>', unsafe_allow_html=True)
    else:
        st.info("La tabla está vacía.")
