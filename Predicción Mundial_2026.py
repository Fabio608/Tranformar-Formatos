import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Simulador Mundial 2026", page_icon="⚽", layout="wide")

# Estilos CSS avanzados para una apariencia premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #003566 0%, #001d3d 100%);
        color: white;
    }

    .container-titulo {
        background: linear-gradient(90deg, #F6B40E 0%, #ffca3a 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    .texto-titulo {
        color: #003566;
        font-size: 48px;
        font-family: 'Bebas Neue', sans-serif;
        margin: 0;
    }

    .stExpander {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }

    /* Estilo de los selectores y inputs */
    .stSelectbox label, .stTextInput label {
        color: #F6B40E !important;
        font-weight: bold !important;
    }

    .stButton>button {
        width: 100%;
        background: #F6B40E !important;
        color: #003566 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        background: #FFFFFF !important;
    }
    </style>
    
    <div class="container-titulo">
        <p class="texto-titulo">PRODE MUNDIAL 2026 - SIMULADOR</p>
    </div>
    """, unsafe_allow_html=True)

def verificar_fecha_limite():
    # Fecha de inicio del mundial: 11 de junio de 2026
    fecha_limite = datetime(2026, 6, 10, 23, 59, 59)
    if datetime.now() > fecha_limite:
        st.error("❌ El periodo de predicciones ha finalizado.")
        return False
    return True

if verificar_fecha_limite():
    with st.sidebar:
        st.image("https://placehold.co/200x100/003566/F6B40E?text=FIFA+2026", use_container_width=True)
        st.header("🏆 Navegación")
        modo = st.radio("Elige tu modo:", ["Mundial Completo", "Mi Grupo Personalizado"])

    if modo == "Mundial Completo":
        # Datos oficiales de los grupos (Simulación basada en proyecciones)
        mundial_2026 = {
            "ZONA A": ["México", "Sudáfrica", "Corea del Sur", "R. Checa"],
            "ZONA B": ["Canadá", "Bosnia", "Qatar", "Suiza"],
            "ZONA C": ["Brasil", "Marruecos", "Haití", "Escocia"],
            "ZONA D": ["Estados Unidos", "Australia", "Paraguay", "Turquía"],
            "ZONA E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
            "ZONA F": ["Paises Bajos", "Japón", "Suecia", "Tunez"],
            "ZONA G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
            "ZONA H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
            "ZONA I": ["Francia", "Senegal", "Irak", "Noruega"],
            "ZONA J": ["Argentina", "Argelia", "Jordania", "Austria"],
            "ZONA K": ["Portugal", "RD Congo", "Uzbequistán", "Colombia"],
            "ZONA L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
        }

        clasificados_finales = {}

        st.info("💡 Selecciona los ganadores de cada partido para calcular las posiciones.")
        
        cols = st.columns(2)
        for idx, (zona, equipos) in enumerate(mundial_2026.items()):
            with cols[idx % 2]:
                with st.expander(f"📍 {zona}"):
                    pts = {e: 0 for e in equipos}
                    # Generar partidos del grupo
                    for i in range(len(equipos)):
                        for j in range(i + 1, len(equipos)):
                            # Importante: key única para evitar DuplicateWidgetID
                            res = st.selectbox(
                                f"{equipos[i]} vs {equipos[j]}",
                                ["Pendiente", f"Gana {equipos[i]}", f"Gana {equipos[j]}", "Empate"],
                                key=f"match_{zona}_{i}_{j}"
                            )
                            if res == f"Gana {equipos[i]}": pts[equipos[i]] += 3
                            elif res == f"Gana {equipos[j]}": pts[equipos[j]] += 3
                            elif res == "Empate":
                                pts[equipos[i]] += 1
                                pts[equipos[j]] += 1
                    
                    # Mostrar tabla de posiciones
                    tabla_df = pd.DataFrame(
                        sorted(pts.items(), key=lambda x: x[1], reverse=True),
                        columns=["Selección", "Puntos"]
                    )
                    st.table(tabla_df)
                    clasificados_finales[zona] = tabla_df.values.tolist()

        st.markdown("---")
        nombre_user = st.text_input("👤 Tu Nombre para el Prode:", placeholder="Ej: Messi_10")
        
        if st.button("🚀 GENERAR RESUMEN PARA WHATSAPP"):
            if all(any(p[1] > 0 for p in pos) for pos in clasificados_finales.values()):
                resumen = f"🏆 *MI PRODE MUNDIAL 2026*\n👤 Usuario: {nombre_user}\n\n"
                for z, pos in clasificados_finales.items():
                    resumen += f"• {z}: 1° {pos[0][0]} | 2° {pos[1][0]}\n"
                
                st.success("¡Copiado al portapapeles (simulado)! Copia el texto de abajo:")
                st.text_area("Texto listo para compartir:", resumen, height=250)
            else:
                st.warning("⚠️ Debes completar al menos un resultado en cada grupo para generar el resumen.")

    else:
        st.subheader("🛠️ Configurador de Grupo Propio")
        st.write("Crea un grupo con las selecciones que quieras y simula los puntos.")
        
        c1, c2 = st.columns(2)
        with c1:
            e1 = st.text_input("Equipo 1", "Argentina", key="e1")
            e2 = st.text_input("Equipo 2", "Francia", key="e2")
        with c2:
            e3 = st.text_input("Equipo 3", "Marruecos", key="e3")
            e4 = st.text_input("Equipo 4", "Japón", key="e4")

        equipos_c = [e1, e2, e3, e4]
        pts_custom = {e: 0 for e in equipos_c}
        
        st.markdown("#### Partidos")
        for i in range(4):
            for j in range(i+1, 4):
                # CORRECCIÓN: Key única usando los nombres de los equipos y sus índices
                label = f"{equipos_c[i]} vs {equipos_c[j]}"
                r = st.selectbox(label, ["-", equipos_c[i], equipos_c[j], "Empate"], key=f"custom_{i}_{j}")
                
                if r == equipos_c[i]: pts_custom[equipos_c[i]] += 3
                elif r == equipos_c[j]: pts_custom[equipos_c[j]] += 3
                elif r == "Empate":
                    pts_custom[equipos_c[i]] += 1
                    pts_custom[equipos_c[j]] += 1
        
        st.markdown("#### Tabla Resultante")
        tabla_final = sorted(pts_custom.items(), key=lambda x: x[1], reverse=True)
        for i, (equipo, puntos) in enumerate(tabla_final, 1):
            clase = "🟢" if i <= 2 else "🔴"
            st.write(f"{clase} **{i}° {equipo}**: {puntos} pts")
