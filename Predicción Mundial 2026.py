import streamlit as st  # <--- ESTO ES LO QUE FALTA O ESTÁ MAL UBICADO
import pandas as pd
import urllib.parse

# La configuración de página DEBE ser el primer comando de Streamlit
st.set_page_config(page_title="Prode WhatsApp", page_icon="🏆")

# --- RESTO DEL CÓDIGO ---

# Inicializar la base de datos temporal si no existe
if "db_participantes" not in st.session_state:
    st.session_state.db_participantes = []

st.title("🏆 Prode del Grupo")

# Menú lateral para navegar
menu = ["🏠 Inicio", "👥 Gestionar Grupo", "⚽ Cargar Resultados", "📊 Tabla de Posiciones"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "🏠 Inicio":
    st.write("### ¡Bienvenido al simulador de posiciones!")
    st.info("Configurá los integrantes y cargá los puntos desde el menú lateral.")

elif choice == "👥 Gestionar Grupo":
    st.header("Integrantes (Máx 20)")
    nuevo_usuario = st.text_input("Nombre del amigo:")
    if st.button("Agregar"):
        if len(st.session_state.db_participantes) < 20:
            # Agregamos un diccionario por cada participante
            st.session_state.db_participantes.append({"Nombre": nuevo_usuario, "Puntos": 0})
            st.success(f"{nuevo_usuario} se unió al grupo.")
        else:
            st.error("Grupo lleno.")
    
    if st.session_state.db_participantes:
        st.write(pd.DataFrame(st.session_state.db_participantes))

elif choice == "⚽ Cargar Resultados":
    st.header("Cargar Jornada")
    if not st.session_state.db_participantes:
        st.warning("No hay integrantes en el grupo.")
    else:
        with st.form("form_puntos"):
            st.write("Seleccioná quiénes sumaron puntos hoy:")
            lista_nombres = [p["Nombre"] for p in st.session_state.db_participantes]
            ganadores = st.multiselect("¿Quiénes acertaron?", lista_nombres)
            puntos_a_sumar = st.number_input("Puntos a otorgar:", min_value=1, value=3)
            
            if st.form_submit_button("Repartir Puntos"):
                for p in st.session_state.db_participantes:
                    if p["Nombre"] in ganadores:
                        p["Puntos"] += puntos_a_sumar
                st.success("¡Puntos actualizados!")

elif choice == "📊 Tabla de Posiciones":
    st.header("Posiciones Actuales")
    if st.session_state.db_participantes:
        df = pd.DataFrame(st.session_state.db_participantes)
        # Ordenamos de mayor a menor puntaje
        df = df.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
        df.index += 1 # Para que el ranking empiece en 1
        st.table(df)
        
        # Generar texto para WhatsApp
        texto_wa = "🏆 *TABLA DEL GRUPO* 🏆\n\n"
        for i, r in df.iterrows():
            texto_wa += f"{i}. {r['Nombre']}: {r['Puntos']} pts\n"
        
        # Botón con link de WhatsApp
        link = f"https://wa.me/?text={urllib.parse.quote(texto_wa)}"
        st.markdown(f"""
            <a href="{link}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; width:100%;">
                    📲 Compartir en WhatsApp
                </button>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.info("La tabla está vacía. Agregá gente en 'Gestionar Grupo'.")
