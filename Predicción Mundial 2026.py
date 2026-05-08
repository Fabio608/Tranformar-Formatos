from datetime import datetime
import sys

def verificar_fecha_limite():
    fecha_limite = datetime(2026, 7, 10, 23, 59, 59)
    fecha_actual = datetime.now()
    if fecha_actual > fecha_limite:
        print("\n❌ LO SIENTO: El plazo terminó el 10 de julio de 2026.")
        return False
    return True

def simular_grupo(nombre_grupo, equipos, es_tercero=False):
    etiqueta = " (CLASIFICACIÓN EXTERNA)" if es_tercero else ""
    print(f"\n=== SIMULANDO {nombre_grupo}{etiqueta} ===")
    print(f"Escribe el NOMBRE del equipo ganador o 'Empate'.\n")

    puntos = {equipo: 0 for equipo in equipos}
    
    # Generar partidos
    partidos = []
    for i in range(len(equipos)):
        for j in range(i + 1, len(equipos)):
            partidos.append((equipos[i], equipos[j]))

    for local, visitante in partidos:
        while True:
            # Pedimos el nombre del equipo o empate
            res = input(f"Partido: {local} vs {visitante} -> Ganador: ").strip().lower()
            
            if res == local.lower():
                puntos[local] += 3
                break
            elif res == visitante.lower():
                puntos[visitante] += 3
                break
            elif res in ['empate', 'x', 'e']:
                puntos[local] += 1
                puntos[visitante] += 1
                break
            else:
                print(f"⚠️ Error. Escribe '{local}', '{visitante}' o 'Empate'.")

    tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n--- POSICIONES {nombre_grupo} ---")
    for i, (equipo, pts) in enumerate(tabla, 1):
        print(f"{i}. {equipo}: {pts} pts")
    
    return tabla[:2] 

# --- INICIO DEL PROGRAMA ---

if not verificar_fecha_limite():
    sys.exit()

mundial_2026 = {
    "ZONA A": ["Mexico", "Sudafrica", "Corea del Sur", "Republica Checa"],
    "ZONA B": ["Canada", "Bosnia", "Qatar", "Suiza"],
    "ZONA C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "ZONA D": ["Estados Unidos", "Australia", "Paraguay", "Turquia"],
    "ZONA E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "ZONA F": ["Paises Bajos", "Japon", "Suecia", "Tunez"],
    "ZONA G": ["Belgica", "Egipto", "Irán", "Nueva Zelanda"],
    "ZONA H": ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"],
    "ZONA I": ["Francia", "Senegal", "Irak", "Noruega"],
    "ZONA J": ["Argentina", "Argelia", "Jordania", "Austria"],
    "ZONA K": ["Portugal", "RD Congo", "Uzbequistan", "Colombia"],
    "ZONA L": ["Inglaterra", "Croacia", "Ghana", "Panama"],
}

zonas_terceros = ["ZONA A", "ZONA B", "ZONA C", "ZONA D"]
clasificados_totales = {}

for nombre, lista_equipos in mundial_2026.items():
    es_zona_tercero = nombre in zonas_terceros
    clasificados = simular_grupo(nombre, lista_equipos, es_tercero=es_zona_tercero)
    clasificados_totales[nombre] = clasificados

print("\n=== EQUIPOS QUE PASAN A LA SIGUIENTE RONDA ===")
for grupo, clasificados in clasificados_totales.items():
    check = " [✓ Terceros]" if grupo in zonas_terceros else ""
    print(f"{grupo}{check}: {clasificados[0][0]} y {clasificados[1][0]}")