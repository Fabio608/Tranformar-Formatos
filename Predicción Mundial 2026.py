import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador de Prode 2026", page_icon="⚽")

st.markdown("<h1 style='text-align: center;'>⚽ Mi Pronóstico Mundial 2026</h1>", unsafe_allow_html=True)
st.write("Completá tus resultados y copialos para enviarlos al grupo.")

# --- 2. DATOS DEL MUNDIAL (Podés agregar más grupos) ---
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

# --- 3. FORMULARIO DE PREDICCIÓN ---
nombre = st.text_input("👤 Tu Nombre / Apodo:", placeholder="Ej: Juan_Gis")

predicciones_texto = []

for zona, equipos in mundial.items():
    with st.expander(f"📅 {zona}", expanded=True):
        for i in range(len(equipos)):
            for j in range(i + 1, len(equipos)):
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
                
                with col1:
                    st.write(f"**{equipos[i]}**")
                with col2:
                    goles_l = st.number_input("Goles", min_value=0, max_value=20, step=1, key=f"L_{zona}_{i}_{j}", label_visibility="collapsed")
                with col3:
                    st.write("vs")
                with col4:
                    goles_v = st.number_input("Goles", min_value=0, max_value=20, step=1, key=f"V_{zona}_{i}_{j}", label_visibility="collapsed")
                with col5:
                    st.write(f"**{equipos[j]}**")
                
                # Guardamos el formato para el mensaje final
                predicciones_texto.append(f"🔹 {equipos[i]} {goles_l} - {goles_v} {equipos[j]}")

# --- 4. GENERACIÓN DEL MENSAJE PARA WHATSAPP ---
st.divider()

if st.button("🚀 GENERAR MENSAJE PARA COPIAR"):
    if nombre:
        # Armamos el bloque de texto final
        mensaje_final = f"🏆 *PRODE MUNDIAL 2026*\n\n"
        mensaje_final += f"👤 *Usuario:* {nombre}\n"
        mensaje_final += "--------------------------\n"
        mensaje_final += "\n".join(predicciones_texto)
        mensaje_final += "\n\n--------------------------\n"
        mensaje_final += "✅ _Enviado desde la App de Prode_"

        # Mostramos el resultado en un cuadro de texto fácil de copiar
        st.subheader("📋 Copiá este mensaje:")
        st.code(mensaje_final, language="text")
        
        st.success("¡Listo! Copiá el texto de arriba y pegalo en el chat de tus amigos.")
        st.balloons()
    else:
        st.error("⚠️ Por favor, poné tu nombre antes de generar el mensaje.")

# --- INFO DE PUNTOS ---
st.sidebar.header("Reglas Sugeridas")
st.sidebar.write("""
- **3 Puntos:** Resultado exacto.
- **1 Punto:** Acertar ganador o empate (pero no el marcador).
- **0 Puntos:** No acertar nada.
""")
