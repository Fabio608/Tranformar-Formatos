import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1551958219-acbc608c6377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.93);
        border-radius: 20px;
        padding: 40px;
        margin-top: 30px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    
    .nombre-equipo {
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: #000000 !important;
    }

    button.step-up, button.step-down { display: none !important; }
    
    div[data-testid="stNumberInput"] { width: 55px !important; margin: 0 auto; }
    
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 2px solid #1a472a !important;
        border-radius: 8px !important;
    }

    input {
        text-align: center !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        color: #1a472a !important;
    }
    
    .guion { font-size: 1.4rem; font-weight: bold; text-align: center; color: #000; }

    h1 { color: #1a472a; text-align: center; font-weight: 900; font-size: 3rem !important; }
    h3 { color: #1a472a; font-weight: 800; border-bottom: 3px solid #1a472a; padding-bottom: 5px; }
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
            tabla.loc[e1, 'PJ'] += 1; tabla.loc[e2, 'PJ'] += 1
            tabla.loc[e1, 'GF'] += g1; tabla.loc[e1, 'GC'] += g2
            tabla.loc[e2, 'GF'] += g2; tabla.loc[e2, 'GC'] += g1
            if g1 > g2: tabla.loc[e1, 'Pts'] += 3
            elif g1 < g2: tabla.loc[e2, 'Pts'] += 3
            else:
                tabla.loc[e1, 'Pts'] += 1; tabla.loc[e2, 'Pts'] += 1
    tabla['DG'] = tabla['GF'] - tabla['GC']
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 4. INTERFAZ ---
if ahora > fecha_limite:
    st.error("❌ El plazo de entrega finalizó.")
else:
    st.markdown(f"**⏳ Tiempo restante:** {tiempo_restante.days} días.")
    nombre = st.text_input("👤 Tu Nombre / Apodo:", placeholder="Tu nombre aquí...")

    predicciones_para_mensaje = []

    for zona, equipos in mundial.items():
        st.subheader(f"📅 {zona}")
        col_partidos, col_tabla = st.columns([1.2, 1])
        resultados_grupo = []
        
        with col_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    c1, c2, c3, c4, c5 = st.columns([2, 0.7, 0.3, 0.7, 2])
                    with c1: st.markdown(f"<p class='nombre-equipo' style='text-align:right;'>{equipos[i]}</p>", unsafe_allow_html=True)
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"g1_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c3: st.markdown("<p class='guion'>-</p>", unsafe_allow_html=True)
                    with c4: g2 = st.number_input("", 0, 20, 0, key=f"g2_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c5: st.markdown(f"<p class='nombre-equipo' style='text-align:left;'>{equipos[j]}</p>", unsafe_allow_html=True)
                    
                    jugado = (g1 > 0 or g2 > 0)
                    resultados_grupo.append((equipos[i], g1, equipos[j], g2, jugado))
                    if jugado: predicciones_para_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
        
        with col_tabla:
            # ESTILO DE LA TABLA
            df_tabla = calcular_tabla(equipos, resultados_grupo)
            
            def resaltar_puntero(s):
                is_max = s == s.max()
                return ['background-color: #28a745; color: white; font-weight: bold' if v else '' for v in is_max]

            st.markdown("<p style='font-weight: bold; color: #1a472a;'>📊 POSICIONES EN VIVO</p>", unsafe_allow_html=True)
            
            # Aplicamos colores y estilos
            estilo_tabla = df_tabla.style.apply(resaltar_puntero, subset=['Pts'])\
                .set_properties(**{'text-align': 'center', 'font-weight': 'bold'})\
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#1a472a'), ('color', 'white'), ('font-size', '14px')]}
                ])
            
            st.dataframe(estilo_tabla, use_container_width=True)

    # --- 5. BOTÓN FINAL ---
    st.divider()
    if st.button("✅ FINALIZAR Y COMPARTIR"):
        if nombre and predicciones_para_mensaje:
            resumen = f"🏆 PRODE MUNDIAL 2026\n👤 Usuario: {nombre}\n" + "-"*20 + "\n"
            resumen += "\n".join(predicciones_para_mensaje)
            st.success("¡Copia este texto y mándalo al grupo!")
            st.code(resumen, language="text")
            st.balloons()
        else:
            st.warning("⚠️ Asegúrate de poner tu nombre y cargar resultados.")
