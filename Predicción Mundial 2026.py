¡Claro que sí! Podemos llevar la app a otro nivel visual y funcional sin complicar la parte técnica.Para que la tabla de posiciones se calcule en tiempo real mientras el usuario carga los goles, usaremos un poco de lógica de Python para procesar los puntos ($3$ por ganar, $1$por empatar) y la diferencia de gol.Aquí tienes el código mejorado. Para el fondo de la Copa del Mundo, incluí un bloque de CSS que busca una imagen estética para que no se vea tan "plana".Pitónimport streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# --- 1. CONFIGURACIÓN Y ESTÉTICA ---
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽", layout="wide")

# CSS para fondo y estilo
st.markdown("""
    <style>
    .main {
        background-image: url("https://images.unsplash.com/photo-1551958219-acbc608c6377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .stApp {
        background: rgba(255, 255, 255, 0.85); /* Capa blanca semi-transparente para leer bien */
        border-radius: 15px;
        padding: 20px;
    }
    h1 { color: #1a472a; text-shadow: 1px 1px 2px #000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🏆 PRODE MUNDIAL 2026 🏆</h1>", unsafe_allow_html=True)

# --- 2. LÓGICA DE TIEMPO (Argentina UTC-3) ---
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

# Función para calcular tabla
def calcular_tabla(equipos, resultados):
    tabla = pd.DataFrame({
        'Equipo': equipos,
        'Pts': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'DG': 0
    }).set_index('Equipo')
    
    for res in resultados:
        e1, g1, e2, g2 = res
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
    # Ordenar por Puntos, luego Diferencia de Gol, luego Goles a Favor
    return tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False)

# --- 4. INTERFAZ ---
if ahora > fecha_limite:
    st.error("❌ El plazo de entrega finalizó el 10 de junio a las 23:59 (Hora Argentina).")
else:
    st.info(f"⏳ Tiempo restante: {tiempo_restante.days} días, {tiempo_restante.seconds//3600} horas.")
    nombre = st.text_input("👤 Ingresa tu nombre:")

    predicciones_para_mensaje = []

    for zona, equipos in mundial.items():
        st.subheader(f"📅 {zona}")
        col_partidos, col_tabla = st.columns([3, 2])
        
        resultados_grupo = []
        
        with col_partidos:
            for i in range(len(equipos)):
                for j in range(i + 1, len(equipos)):
                    c1, c2, c3, c4, c5 = st.columns([2, 1, 0.5, 1, 2])
                    with c1: st.write(f"**{equipos[i]}**")
                    with c2: g1 = st.number_input("", 0, 20, 0, key=f"g1_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c3: st.write("-")
                    with c4: g2 = st.number_input("", 0, 20, 0, key=g2_{zona}_{i}_{j}", label_visibility="collapsed")
                    with c5: st.write(f"**{equipos[j]}**")
                    
                    resultados_grupo.append((equipos[i], g1, equipos[j], g2))
                    predicciones_para_mensaje.append(f"{equipos[i]} {g1}-{g2} {equipos[j]}")
        
        with col_tabla:
            st.markdown(f"**Tabla de Posiciones {zona}**")
            tabla_f = calcular_tabla(equipos, resultados_grupo)
            st.dataframe(tabla_f, use_container_width=True)

    # --- 5. BOTÓN FINAL ---
    st.divider()
    if st.button("✅ FINALIZAR Y COMPARTIR"):
        if nombre:
            resumen = f"🏆 PRODE MUNDIAL 2026\n👤 Usuario: {nombre}\n" + "-"*20 + "\n"
            resumen += "\n".join(predicciones_para_mensaje)
            
            st.success("¡Pronóstico generado con éxito!")
            st.code(resumen, language="text")
            st.balloons()
        else:
            st.warning("⚠️ Por favor, ingresa tu nombre antes de finalizar.")
