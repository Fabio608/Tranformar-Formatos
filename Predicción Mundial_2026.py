import streamlit as st
from datetime import datetime
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽", layout="wide")

# --- ESTILOS CSS AVANZADOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;700&display=swap');
    
    /* Fondo General */
    .stApp {
        background: linear-gradient(135deg, #f0f2f5 0%, #c9d6ff 100%);
    }

    /* Título Principal */
    .container-titulo {
        background: linear-gradient(90deg, #003566 0%, #00509d 50%, #003566 100%);
        padding: 30px;
        border-radius: 20px;
        border-bottom: 5px solid #F6B40E;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
    }
    
    .texto-titulo {
        color: #FFFFFF;
        font-size: 42px;
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Subtítulos de Secciones */
    .subtitulo-seccion {
        font-family: 'Bebas Neue', sans-serif;
        color: #003566;
        font-size: 30px;
        border-left: 8px solid #F6B40E;
        padding-left: 15px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Tarjetas de Grupos */
    .stExpander {
        background-color: white !important;
        border-radius: 15px !important;
        border: 1px solid #ddd !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05) !important;
    }

    /* Botones Personalizados */
    .stButton>button {
        background: linear-gradient(90deg, #F6B40E 0%, #ffca3a 100%) !important;
        color: #003566 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        height: 50px !important;
        width: 100% !important;
        font-size: 18px !important;
        transition: 0.3s !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    
    <div class="container-titulo">
        <p class="texto-titulo">⚽ MIS PREDICCIONES - MUNDIAL 2026 - EEUU - CANADA - MEXICO</p>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE FECHA ---
def verificar_fecha_limite():
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ El plazo para cargar predicciones terminó.")
        return False
    return True

if verificar_fecha_limite():
    
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.header("🛠️ Herramientas")
        modo = st.radio("Selecciona modo:", ["Simulador Mundial Completo", "Crea tu Propio Grupo"])
        st.info("Configura los resultados para ver quién avanza.")

    if modo == "Simulador Mundial Completo":
        st.markdown('<p class="subtitulo-seccion">🏆 FASE DE GRUPOS OFICIAL</p>', unsafe_allow_html=True)
        
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

        clasificados_finales = {}

        cols = st.columns(2)
        for idx, (nombre_zona, equipos) in enumerate(mundial_2026.items()):
            col_target = cols[idx % 2]
            with col_target:
                with st.expander(f"📍 {nombre_zona}: {', '.join(equipos)}"):
                    puntos = {equipo: 0 for equipo in equipos}
                    
                    for i in range(len(equipos)):
                        for j in range(i + 1, len(equipos)):
                            local, visita = equipos[i], equipos[j]
                            res = st.selectbox(f"{local} vs {visita}",
                                             ["Pendiente", f"Gana {local}", f"Gana {visita}", "Empate"],
                                             key=f"full_{nombre_zona}_{local}_{visita}")
                            
                            if res == f"Gana {local}": puntos[local] += 3
                            elif res == f"Gana {visita}": puntos[visita] += 3
                            elif res == "Empate":
                                puntos[local] += 1
                                puntos[visita] += 1
                    
                    # Tabla resumen del grupo
                    tabla_ord = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
                    df_tabla = pd.DataFrame(tabla_ord, columns=["Equipo", "Pts"])
                    st.table(df_tabla)
                    
                    if any(p > 0 for p in puntos.values()):
                        clasificados_finales[nombre_zona] = tabla_ord

        st.write("---")
        nombre_usuario = st.text_input("✍️ Tu nombre para el resumen:", placeholder="Ej: Fabio")

        if st.button("Generar resumen y Compartir"):
            if len(clasificados_finales) == 12:
                st.success("✅ ¡Simulación Guardada!")
                autor = nombre_usuario if nombre_usuario else "Invitado"
                resumen_texto = f"⚽ PREDICCIONES MUNDIAL 2026 🏆\n👤 Usuario: {autor}\n" + "-"*20 + "\n"
                for zona, posiciones in clasificados_finales.items():
                    resumen_texto += f"📍 {zona}: 1° {posiciones[0][0]}, 2° {posiciones[1][0]}\n"
                st.text_area("Copia esto:", resumen_texto, height=250)
            else:
                st.warning(f"Faltan completar {12 - len(clasificados_finales)} grupos.")

    else:
        st.markdown('<p class="subtitulo-seccion">🛠️ CREADOR DE GRUPO PERSONALIZADO</p>', unsafe_allow_html=True)
        st.info("Escribe los nombres de 4 equipos para armar tu propia zona de competencia.")
        
        c1, c2, c3, c4 = st.columns(4)
        e1 = c1.text_input("Equipo 1", "Mi Equipo A")
        e2 = c2.text_input("Equipo 2", "Mi Equipo B")
        e3 = c3.text_input("Equipo 3", "Mi Equipo C")
        e4 = c4.text_input("Equipo 4", "Mi Equipo D")
        
        equipos_custom = [e1, e2, e3, e4]
        pts_custom = {e: 0 for e in equipos_custom}
        
        st.markdown("### 🏟️ Simular Partidos")
        
        # Generar partidos dinámicos
        matches_cols = st.columns(3)
        match_idx = 0
        for i in range(len(equipos_custom)):
            for j in range(i + 1, len(equipos_custom)):
                with matches_cols[match_idx % 3]:
                    res_c = st.selectbox(f"{equipos_custom[i]} vs {equipos_custom[j]}",
                                       ["Pendiente", f"Gana {equipos_custom[i]}", f"Gana {equipos_custom[j]}", "Empate"],
                                       key=f"custom_match_{i}_{j}")
                    if res_c == f"Gana {equipos_custom[i]}": pts_custom[equipos_custom[i]] += 3
                    elif res_c == f"Gana {equipos_custom[j]}": pts_custom[equipos_custom[j]] += 3
                    elif res_c == "Empate":
                        pts_custom[equipos_custom[i]] += 1
                        pts_custom[equipos_custom[j]] += 1
                match_idx += 1

        st.markdown("### 📈 Tabla de Posiciones Final")
        tabla_custom = sorted(pts_custom.items(), key=lambda x: x[1], reverse=True)
        
        # Mostrar con colores según posición
        for pos, (equipo, pts) in enumerate(tabla_custom, 1):
            color_banda = "#4CAF50" if pos <= 2 else "#FF5252" # Verde clasificados, Rojo eliminados
            st.markdown(f"""
                <div style="background-color: {color_banda}; color: white; padding: 10px; border-radius: 10px; margin-bottom: 5px; display: flex; justify-content: space-between;">
                    <span><b>{pos}° {equipo}</b></span>
                    <span>{pts} Puntos</span>
                </div>
            """, unsafe_allow_html=True)
