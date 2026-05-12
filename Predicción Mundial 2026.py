import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽")

# --- TÍTULO PERSONALIZADO (GOOGLE FONTS Y ESTILO ARGENTINA) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    
    .container-titulo {
        background: linear-gradient(180deg, #74ACDF 30%, #FFFFFF 30%, #FFFFFF 70%, #74ACDF 70%);
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #F6B40E;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    .texto-titulo {
        color: #003566;
        font-size: 28px;
        font-family: 'Bebas Neue', sans-serif;
        font-weight: bold;
        letter-spacing: 1px;
        margin: 0;
        text-shadow: 1px 1px 0px #fff;
        line-height: 1.2;
    }
    </style>
    
    <div class="container-titulo">
        <p class="texto-titulo">⚽ MIS PREDICCIONES - MUNDIAL 2026 - EEUU - CANADA - MEXICO</p>
    </div>
    """, unsafe_allow_html=True)

# --- FUNCIONES ---
def verificar_fecha_limite():
    # Fecha límite: Comienzo del mundial
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ El plazo para cargar predicciones terminó el 10 de junio.")
        return False
    return True

if verificar_fecha_limite():
    mundial_2026 = {
        "ZONA A": ["México", "Sudáfrica", "Corea del Sur", "República Checa"],
        "ZONA B": ["Canadá", "Bosnia", "Qatar", "Suiza"],
        "ZONA C": ["Brasil", "Marruecos", "Haití", "Escocia"],
        "ZONA D": ["Estados Unidos", "Australia", "Paraguay", "Turquía"],
        "ZONA E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
        "ZONA F": ["Paises Bajos", "Japón", "Suecia", "Tunez"],
        "ZONA G": ["Belgica", "Egipto", "Irán", "Nueva Zelanda"],
        "ZONA H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
        "ZONA I": ["Francia", "Senegal", "Irak", "Noruega"],
        "ZONA J": ["Argentina", "Argelia", "Jordania", "Austria"],
        "ZONA K": ["Portugal", "RD Congo", "Uzbequistan", "Colombia"],
        "ZONA L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
    }
    
    st.info("💡 Completa los partidos de cada zona para generar tu resumen final.")

    clasificados_finales = {}

    for nombre_zona, equipos in mundial_2026.items():
        equipos_str = ", ".join(equipos)
        with st.expander(f"🏆 {nombre_zona} ({equipos_str})"):
            puntos = {equipo: 0 for equipo in equipos}
            
            # Generar enfrentamientos de todos contra todos en el grupo
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    local, visita = equipos[i], equipos[j]
                    res = st.selectbox(f"{local} vs {visita}",
                                     ["Pendiente", f"Gana {local}", f"Gana {visita}", "Empate"],
                                     key=f"{nombre_zona}_{local}_{visita}")
                    
                    if res == f"Gana {local}": puntos[local] += 3
                    elif res == f"Gana {visita}": puntos[visita] += 3
                    elif res == "Empate":
                        puntos[local] += 1
                        puntos[visita] += 1
            
            tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            st.write("**Posiciones Temporales:**")
            for pos, (equipo, pts) in enumerate(tabla, 1):
                st.write(f"{pos}. {equipo}: {pts} pts")
            
            # Guardamos la zona si ya tiene algún resultado cargado
            if any(p > 0 for p in puntos.values()):
                clasificados_finales[nombre_zona] = tabla

    st.write("---")
    
    nombre_usuario = st.text_input("✍️ Escribe tu nombre para el resumen:", placeholder="Ej: Fabio")

    if st.button("🏆 Compartir y Generar resumen"):
        if len(clasificados_finales) == 12:
            st.success("✅ ¡Simulación Completa!")
            autor = nombre_usuario if nombre_usuario else "Invitado"
            
            # Construcción del mensaje de texto
            resumen_texto = f"⚽ PREDICCIONES MUNDIAL 2026 🏆\n"
            resumen_texto += f"👤 Usuario: {autor}\n"
            resumen_texto += "--------------------------------\n"
            
            for zona, posiciones in clasificados_finales.items():
                p1, p2, p3 = posiciones[0][0], posiciones[1][0], posiciones[2][0]
                resumen_texto += f"📍 {zona}: 1° {p1}, 2° {p2} (3° {p3})\n"
            
            st.write(f"### 📝 Resumen de {autor}:")
            st.text_area("Copia este texto para WhatsApp/Redes:", resumen_texto, height=350)
        else:
            # Notificación si faltan zonas por completar
            st.warning(f"Faltan grupos por completar ({len(clasificados_finales)}/12).")
