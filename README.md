import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽")

def verificar_fecha_limite():
    fecha_limite = datetime(2026, 7, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ LO SIENTO: El plazo para cargar predicciones terminó.")
        return False
    return True

# Título de la App
st.title("⚽ Simulador Mundial 2026")

if verificar_fecha_limite():
    
    # Definición de grupos y zonas
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
    
    zonas_terceros = ["ZONA A", "ZONA B", "ZONA C", "ZONA D"]
    st.info(f"Zonas habilitadas para terceros: {', '.join(zonas_terceros)}")

    clasificados_finales = {}

    # Crear una pestaña o sección por grupo
    for nombre_zona, equipos in mundial_2026.items():
        with st.expander(f"Simular {nombre_zona} {'✅ (Terceros)' if nombre_zona in zonas_terceros else ''}"):
            puntos = {equipo: 0 for equipo in equipos}
            
            # Generar partidos del grupo
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    local, visita = equipos[i], equipos[j]
                    
                    # Selector visual en lugar de input()
                    res = st.radio(
                        f"Resultado: {local} vs {visita}",
                        ["Pendiente", local, visita, "Empate"],
                        key=f"{nombre_zona}_{local}_{visita}"
                    )
                    
                    if res == local: puntos[local] += 3
                    elif res == visita: puntos[visita] += 3
                    elif res == "Empate":
                        puntos[local] += 1
                        puntos[visita] += 1
            
            # Tabla de posiciones automática
            tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            st.write("**Posiciones Temporales:**")
            for pos, (equipo, pts) in enumerate(tabla, 1):
                st.text(f"{pos}. {equipo}: {pts} pts")
            
            clasificados_finales[nombre_zona] = [tabla[0][0], tabla[1][0]]

    # Botón final para ver todos los clasificados
    if st.button("Generar Resumen de Clasificados"):
        st.header("🏆 Equipos en Octavos")
        for grupo, clasificados in clasificados_finales.items():
            st.write(f"**{grupo}:** {clasificados[0]} y {clasificados[1]}")
