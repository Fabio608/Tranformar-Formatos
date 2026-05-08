import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽")

def verificar_fecha_limite():
    # FECHA LÍMITE: 10 de junio de 2026
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ Plazo terminado el 10 de junio.")
        return False
    return True

st.title("⚽ Mis Predicciones - Mundial 2026")

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
    
    zonas_terceros = ["ZONA A", "ZONA B", "ZONA C", "ZONA D"]
    st.info(f"💡 **Zonas para Terceros:** {', '.join(zonas_terceros)}")

    clasificados_finales = {}

    for nombre_zona, equipos in mundial_2026.items():
        # --- AQUÍ AGREGO LOS EQUIPOS ENTRE PARÉNTESIS ---
        equipos_str = ", ".join(equipos)
        check = " ✅" if nombre_zona in zonas_terceros else ""
        
        with st.expander(f"{nombre_zona} ({equipos_str}){check}"):
            puntos = {equipo: 0 for equipo in equipos}
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
            if len(tabla) >= 2:
                clasificados_finales[nombre_zona] = [tabla[0][0], tabla[1][0]]

    st.write("---")
    
    if st.button("🏆 FINALIZAR Y GENERAR RESUMEN"):
        if len(clasificados_finales) == len(mundial_2026):
            st.success("¡Predicción completada!")
            
            # Crear el texto para compartir
            texto_compartir = "🏆 MIS CLASIFICADOS MUNDIAL 2026 ⚽\n\n"
            for zona, equipos in clasificados_finales.items():
                texto_compartir += f"📍 {zona}: {equipos[0]} y {equipos[1]}\n"
            
            st.text_area("Copia este resumen para compartir:", texto_compartir, height=300)
            
            # Mostrar visualmente
            cols = st.columns(2)
            for idx, (zona, clas) in enumerate(clasificados_finales.items()):
                with cols[idx % 2]:
                    st.write(f"**{zona}**: {clas[0]} y {clas[1]}")
        else:
            st.warning(f"Faltan grupos por completar ({len(clasificados_finales)}/12).")