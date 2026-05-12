import streamlit as st
from datetime import datetime, timezone, timedelta

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽")

# --- SISTEMA DE ACCESO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Intentamos obtener la contraseña de los Secrets, si no existe usamos una fija
# Esto evita que la app se bloquee si el panel de Streamlit falla
try:
    PASSWORD_SECRETA = st.secrets.get("PASSWORD", "Mundial2026")
except Exception:
    PASSWORD_SECRETA = "Mundial2026"

if not st.session_state.autenticado:
    st.title("🔐 Acceso Privado")
    st.write("Esta aplicación es exclusiva. Por favor, ingresa la clave de acceso.")
    
    # Usamos un formulario para que sea más robusto al presionar Enter
    with st.form("login_form"):
        clave = st.text_input("Contraseña:", type="password")
        boton_ingresar = st.form_submit_button("Ingresar")
        
        if boton_ingresar:
            if clave == PASSWORD_SECRETA:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Clave incorrecta. Inténtalo de nuevo.")
    st.stop()

# --- FUNCIONES ---
def verificar_fecha_limite():
    # Ajustamos a la zona horaria de Argentina (donde estás vos)
    AR = timezone(timedelta(hours=-3))
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
    if datetime.now(AR) > fecha_limite:
        st.error("❌ El plazo para cargar predicciones terminó el 10 de junio.")
        return False
    return True

# --- TÍTULO (bandera argentina) ---
st.markdown("""
<div style="
background: linear-gradient(180deg, #74ACDF 30%, #FFFFFF 30%, #FFFFFF 70%, #74ACDF 70%);
padding: 15px;
border-radius: 10px;
border: 2px solid #F6B40E;
text-align: center;
margin-bottom: 20px;
">
<h2 style="color: #003566; margin: 0; font-family: sans-serif;">⚽ Mis Predicciones - Mundial 2026 🇦🇷</h2>
</div>
""", unsafe_allow_html=True)

if verificar_fecha_limite():
    mundial_2026 = {
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

    st.info("💡 Completa los partidos de cada zona para generar tu resumen final.")

    clasificados_finales = {}

    # Generar grupos
    for nombre_zona, equipos in mundial_2026.items():
        equipos_str = " - ".join(equipos)
        with st.expander(f"📍 {nombre_zona} ({equipos_str})"):
            puntos = {equipo: 0 for equipo in equipos}
            total_partidos = 6 # 4 equipos = 6 partidos por zona
            partidos_completados = 0

            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    local, visita = equipos[i], equipos[j]
                    res = st.selectbox(
                        f"{local} vs {visita}",
                        ["Pendiente", f"Gana {local}", f"Gana {visita}", "Empate"],
                        key=f"{nombre_zona}_{local}_{visita}"
                    )
                    
                    if res != "Pendiente":
                        partidos_completados += 1
                        if res == f"Gana {local}":
                            puntos[local] += 3
                        elif res == f"Gana {visita}":
                            puntos[visita] += 3
                        elif res == "Empate":
                            puntos[local] += 1
                            puntos[visita] += 1

            # Tabla de posiciones visual
            tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            st.write(f"**Posiciones actualizadas:**")
            for pos, (equipo, pts) in enumerate(tabla, 1):
                icono = "✅" if pos <= 2 else "❌"
                st.write(f"{pos}. {equipo}: **{pts} pts** {icono if partidos_completados == 6 else ''}")

            if partidos_completados == total_partidos:
                clasificados_finales[nombre_zona] = tabla

    # Barra de progreso general
    progreso = len(clasificados_finales)
    st.progress(progreso / 12, text=f"Progreso: {progreso} de 12 grupos completados")

    st.write("---")

    nombre_usuario = st.text_input("✍️ Tu nombre para el resumen:", placeholder="Ej: Fabio")

    if st.button("🏆 GENERAR RESUMEN FINAL"):
        if len(clasificados_finales) == 12:
            st.success("✅ ¡Simulación Completa!")
            autor = nombre_usuario if nombre_usuario else "Invitado"
            
            resumen_texto = f"⚽ PREDICCIONES MUNDIAL 2026 🏆\n"
            resumen_texto += f"👤 Usuario: {autor}\n"
            resumen_texto += "--------------------------------\n"
            
            for zona, posiciones in clasificados_finales.items():
                p1, p2 = posiciones[0][0], posiciones[1][0]
                resumen_texto += f"📍 {zona}: 1° {p1} | 2° {p2}\n"
            
            st.write(f"### 📝 Resumen de {autor}:")
            st.text_area("Copia esto para compartir:", resumen_texto, height=300)
        else:
            st.warning(f"Faltan completar {12 - len(clasificados_finales)} grupos para finalizar.")
