import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽")

# --- SISTEMA DE ACCESO (CONTRASEÑA) ---
# Cambia "Mundial2026" por la clave que quieras darle a tus compañeros
PASSWORD_SECRETA = "Mundial2026"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso Privado")
    st.write("Esta aplicación es exclusiva. Por favor, ingresa la clave de acceso.")
    clave = st.text_input("Contraseña:", type="password")
    if st.button("Ingresar"):
        if clave == PASSWORD_SECRETA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Clave incorrecta. Solicítala al administrador.")
    st.stop() # Bloquea el resto de la app hasta que pongan la clave

# --- EL RESTO DE TU CÓDIGO (SOLO SE VE SI ESTÁ AUTENTICADO) ---

def verificar_fecha_limite():
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ El plazo para cargar predicciones terminó el 10 de junio.")
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
    
    st.info("💡 Completa los partidos de cada zona para generar tu resumen final.")

    clasificados_finales = {}

    for nombre_zona, equipos in mundial_2026.items():
        equipos_str = ", ".join(equipos)
        with st.expander(f"{nombre_zona} ({equipos_str})"):
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
            st.write("**Posiciones:**")
            for pos, (equipo, pts) in enumerate(tabla, 1):
                st.write(f"{pos}. {equipo}: {pts} pts")
            
            if any(p > 0 for p in puntos.values()):
                clasificados_finales[nombre_zona] = tabla

    st.write("---")
    
    nombre_usuario = st.text_input("✍️ Escribe tu nombre para el resumen:", placeholder="Ej: Fabio")

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
            
            st.write(f"### 📝 Resumen de {autor}:")
            st.text_area("Copia este texto para WhatsApp/Redes:", resumen_texto, height=350)
        else:
            st.warning(f"Faltan grupos por completar ({len(clasificados_finales)}/12).")