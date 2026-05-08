import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
# El page_icon puede ser un emoji o un link a una imagen
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="🏆", layout="centered")

def verificar_fecha_limite():
    # FECHA LÍMITE: 10 de junio de 2026
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ El plazo para cargar predicciones terminó el 10 de junio.")
        return False
    return True

# Diccionario de banderas para que el código sea limpio
banderas = {
    "México": "🇲🇽", "Sudáfrica": "🇿🇦", "Corea del Sur": "🇰🇷", "República Checa": "🇨🇿",
    "Canadá": "🇨🇦", "Bosnia": "🇧🇦", "Qatar": "🇶🇦", "Suiza": "🇨🇭",
    "Brasil": "🇧🇷", "Marruecos": "🇲🇦", "Haití": "🇭🇹", "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Estados Unidos": "🇺🇸", "Australia": "🇦🇺", "Paraguay": "🇵🇾", "Turquía": "🇹🇷",
    "Alemania": "🇩🇪", "Curazao": "🇨🇼", "Costa de Marfil": "🇨🇮", "Ecuador": "🇪🇨",
    "Paises Bajos": "🇳🇱", "Japón": "🇯🇵", "Suecia": "🇸🇪", "Tunez": "🇹🇳",
    "Belgica": "🇧🇪", "Egipto": "🇪🇬", "Irán": "🇮🇷", "Nueva Zelanda": "🇳🇿",
    "España": "🇪🇸", "Cabo Verde": "🇨🇻", "Arabia Saudita": "🇸🇦", "Uruguay": "🇺🇾",
    "Francia": "🇫🇷", "Senegal": "🇸🇳", "Irak": "🇮🇶", "Noruega": "🇳🇴",
    "Argentina": "🇦🇷", "Argelia": "🇩🇿", "Jordania": "🇯🇴", "Austria": "🇦🇹",
    "Portugal": "🇵🇹", "RD Congo": "🇨🇩", "Uzbequistan": "🇺🇿", "Colombia": "🇨🇴",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croacia": "🇭🇷", "Ghana": "🇬🇭", "Panamá": "🇵🇦"
}

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
    
    st.info("💡 Haz clic en cada zona para desplegar los partidos y elegir tus ganadores.")

    clasificados_finales = {}

    for nombre_zona, equipos in mundial_2026.items():
        # Título del grupo con banderas
        tit_equipos = " ".join([f"{banderas.get(e, '')}" for e in equipos])
        
        with st.expander(f"📍 {nombre_zona} | {tit_equipos}"):
            puntos = {equipo: 0 for equipo in equipos}
            
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    loc, vis = equipos[i], equipos[j]
                    b_loc, b_vis = banderas.get(loc, ""), banderas.get(vis, "")
                    
                    res = st.selectbox(
                        f"{b_loc} {loc} vs {vis} {b_vis}",
                        ["Pendiente", f"Gana {loc}", f"Gana {vis}", "Empate"],
                        key=f"{nombre_zona}_{loc}_{vis}"
                    )
                    
                    if res == f"Gana {loc}": puntos[loc] += 3
                    elif res == f"Gana {vis}": puntos[vis] += 3
                    elif res == "Empate":
                        puntos[loc] += 1
                        puntos[vis] += 1
            
            # Tabla visual
            tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            st.write("---")
            st.markdown("**Posiciones actualizadas:**")
            for pos, (equipo, pts) in enumerate(tabla, 1):
                st.write(f"{pos}. {banderas.get(equipo, '')} {equipo}: **{pts} pts**")
            
            if any(p > 0 for p in puntos.values()):
                clasificados_finales[nombre_zona] = tabla

    st.write("---")
    nombre_usuario = st.text_input("✍️ Tu nombre para el resumen:", placeholder="Ej: Fabio")

    if st.button("🏆 FINALIZAR Y COMPARTIR"):
        if len(clasificados_finales) == 12:
            st.success("✅ ¡Simulación Completa!")
            autor = nombre_usuario if nombre_usuario else "Invitado"
            
            resumen_texto = f"⚽ PREDICCIONES MUNDIAL 2026 🏆\n"
            resumen_texto += f"👤 Usuario: {autor}\n"
            resumen_texto += "--------------------------------\n"
            
            for zona, posiciones in clasificados_finales.items():
                p1, p2, p3 = posiciones[0][0], posiciones[1][0], posiciones[2][0]
                resumen_texto += f"📍 {zona}: 1° {p1}, 2° {p2} (3° {p3})\n"
            
            st.subheader(f"📝 Resumen de {autor}")
            st.text_area("Copia este texto:", resumen_texto, height=300)
        else:
            st.warning(f"Faltan grupos por completar ({len(clasificados_finales)}/12).")