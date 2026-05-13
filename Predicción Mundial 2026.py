import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽", layout="wide")

# CSS Ajustado para quitar botones + y - y achicar más el cuadro
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1551958219-acbc608c6377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 30px;
        margin-top: 50px;
    }
    
    /* ELIMINA LOS BOTONES + y - */
    button.step-up, button.step-down {
        display: none !important;
    }
    
    /* ACHICA EL CUADRO Y CENTRA EL NÚMERO */
    div[data-testid="stNumberInput"] {
        width: 45px !important;
        margin: 0 auto;
    }
    
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #f0f2f6 !important;
        border-radius: 5px !important;
    }

    input {
        text-align: center !important;
        padding: 5px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    
    h1 { color: #1a472a; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏆 PRODE MUNDIAL 2026 </h1>", unsafe_allow_html=True)

# --- 2. LÓGICA DE TIEMPO ---
AR = timezone(timedelta(hours=-3))
fecha_limite = datetime(2026, 6, 10, 23, 59, 59, tzinfo=AR)
ahora = datetime.now(AR)
tiempo_restante = fecha_limite - ahora

# --- 3. DEFINICIÓN DE GRUPOS ---
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

def calcular_tabla(equipos, resultados):
    tabla = pd.DataFrame({
        'Equipo': equipos,
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    for res in resultados:
        e1, g1, e2, g2, jugado = res
        if jugado:
            tabla.loc[e1, 'PJ'] += 1
            tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'GF'] += g1
            tabla.loc[e1, 'GC'] += g2
            tabla.loc[e2, 'GF'] += g2
            tabla.loc[e2, 'GC'] += g1
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g1 < g2: tabla.loc[e2, 'Pts'] += 3
            else:
                tabla.loc[e1, 'Pts'] += 1
                tabla.loc[e2, 'Pts'] += 1
    tabla['DG'] = tabla['GF'] - tabla['GC']
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 4. INTERFAZ ---
if ahora > fecha_limite:
    st.error("❌ El plazo de entrega finalizó.")
else:
    st.info(f"⏳ Tienes tiempo hasta el 10 de junio. Faltan: {tiempo_restante.days} días.")
    nombre = st.text_input("👤 Tu Nombre:")

    predicciones_para_mensaje = []

    for zona, equipos in mundial.items():
        st.subheader(f"📅 {zona}")
        col_partidos, col_tabla = st.columns([1.2, 1])
        resultados_grupo = []
        
        with col_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    # Columnas optimizadas
                    c1, c2, c3, c4, c5 = st.columns([2, 0.6, 0.2, 0.6, 2])
                    with c1: st.markdown(f"<p style='text-align:right; margin-top:5px;'>{equipos[i]}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"g1_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c3: st.markdown("<p style='text-align:center; margin-top:5px;'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"g2_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c5: st.markdown(f"<p style='text-align:left; margin-top:5px;'>{equipos[j]}</p>", unsafe_allow_html=True)
                    
                    # Detectar si el usuario escribió algo (incluso 0)
                    jugado = (g1 > 0 or g2 > 0)
                    resultados_grupo.append((equipos[i], g1, equipos[j], g2, jugado))
                    if jugado:
                        predicciones_para_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
        
        with col_tabla:
            st.write("📊 Clasificación:")
            tabla_f = calcular_tabla(equipos, resultados_grupo)
            st.dataframe(tabla_f, use_container_width=True)

    # --- 5. BOTÓN FINAL ---
    st.divider()
    if st.button("✅ FINALIZAR Y COMPARTIR"):
        if nombre and predicciones_para_mensaje:
            resumen = f"🏆 PRODE MUNDIAL 2026\n👤 Usuario: {nombre}\n" + "-"*20 + "\n"
            resumen += "\n".join(predicciones_para_mensaje)
            st.success("¡Pronóstico generado con éxito!")
            st.code(resumen, language="text")
            st.balloons()
        elif not nombre:
            st.warning("⚠️ Por favor, poné tu nombre.")
        else:
            st.warning("⚠️ Cargá al menos un resultado.")
