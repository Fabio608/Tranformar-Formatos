import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽")

def verificar_fecha_limite():
    # FECHA LÍMITE: 10 de junio de 2026 a las 23:59:59
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    fecha_actual = datetime.now()
    
    if fecha_actual > fecha_limite:
        st.error("❌ LO SIENTO: El plazo para cargar predicciones terminó el 10 de junio a las 23:59.")
        return False
    return True

st.title("⚽ Simulador Mundial 2026")

if verificar_fecha_limite():
    # Definición de grupos y zonas
    mundial_2026 = {
        "ZONA A": ["Mexico", "Sudafrica", "Corea del Sur", "Republica Checa"],
        "ZONA B": ["Canada", "Bosnia", "Qatar", "Suiza"],
        "ZONA C": ["Brasil", "Marruecos", "Haiti", "Escocia"],
        "ZONA D": ["Estados Unidos", "Australia", "Paraguay", "Turquia"],
        "ZONA E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
        "ZONA F": ["Paises Bajos", "Japon", "Suecia", "Tunez"],
        "ZONA G": ["Belgica", "Egipto", "Iran", "Nueva Zelanda"],
        "ZONA H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
        "ZONA I": ["Francia", "Senegal", "Irak", "Noruega"],
        "ZONA J": ["Argentina", "Argelia", "Jordania", "Austria"],
        "ZONA K": ["Portugal", "RD Congo", "Uzbequistan", "Colombia"],
        "ZONA L": ["Inglaterra", "Croacia", "Ghana", "Panama"],
    }
    
    # Zonas habilitadas para terceros
    zonas_terceros = ["ZONA A", "ZONA B", "ZONA C", "ZONA D"]
    st.info(f"💡 **Zonas para Terceros:** {', '.join(zonas_terceros)}")

    clasificados_finales = {}

    # Simulación visual por grupos
    for nombre_zona, equipos in mundial_2026.items():
        es_tercero = " ✅ (Terceros)" if nombre_zona in zonas_terceros else ""
        
        with st.expander(f"Simular {nombre_zona}{es_tercero}"):
            puntos = {equipo: 0 for equipo in equipos}
            
            # Partidos dentro del grupo
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    local, visita = equipos[i], equipos[j]
                    
                    res = st.selectbox(
                        f"Partido: {local} vs {visita}",
                        ["Pendiente", f"Gana {local}", f"Gana {visita}", "Empate"],
                        key=f"{nombre_zona}_{local}_{visita}"
                    )
                    
                    if res == f"Gana {local}": puntos[local] += 3
                    elif res == f"Gana {visita}": puntos[visita] += 3
                    elif res == "Empate":
                        puntos[local] += 1
                        puntos[visita] += 1
            
            # Tabla ordenada
            tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            
            st.write("---")
            st.write(f"**Tabla de Posiciones {nombre_zona}:**")
            for pos, (equipo, pts) in enumerate(tabla, 1):
                st.write(f"{pos}. {equipo}: {pts} pts")
            
            # Guardamos los 2 primeros
            if len(tabla) >= 2:
                clasificados_finales[nombre_zona] = [tabla[0][0], tabla[1][0]]

    st.write("---")
    
    if st.button("🏆 MOSTRAR TODOS LOS CLASIFICADOS"):
        if len(clasificados_finales) > 0:
            st.header("Equipos que pasan a la siguiente ronda")
            cols = st.columns(2)
            for idx, (grupo, clas) in enumerate(clasificados_finales.items()):
                with cols[idx % 2]:
                    check = " ⭐" if grupo in zonas_terceros else ""
                    st.success(f"**{grupo}{check}:**\n1. {clas[0]}\n2. {clas[1]}")
        else:
            st.warning("Completa al menos un grupo para ver resultados.")