import moviepy.editor as mp
import whisper
import os
import math

# Función auxiliar para convertir segundos al formato de tiempo de los archivos .srt
def formato_srt_tiempo(segundos):
    horas = math.floor(segundos / 3600)
    segundos %= 3600
    minutos = math.floor(segundos / 60)
    segundos %= 60
    milisegundos = round((segundos - math.floor(segundos)) * 1000)
    segundos = math.floor(segundos)
    # Formato: 00:00:00,000
    return f"{horas:02d}:{minutos:02d}:{segundos:02d},{milisegundos:03d}"

def video_a_srt(ruta_video, ruta_audio_temporal="audio_temp.wav", archivo_salida="subtitulos.srt"):
    print("1. Extrayendo audio del video...")
    try:
        video = mp.VideoFileClip(ruta_video)
        video.audio.write_audiofile(ruta_audio_temporal, logger=None)
    except Exception as e:
        return f"Error al extraer audio: {e}"

    print("2. Cargando modelo de inteligencia artificial (local)...")
    modelo = whisper.load_model("base") # Puedes usar "small" o "medium" para mayor precisión

    print("3. Transcribiendo y generando tiempos...")
    resultado = modelo.transcribe(ruta_audio_temporal, language="es")
    
    print("4. Creando archivo .srt...")
    # Whisper guarda los fragmentos con tiempo en la clave "segments"
    segmentos = resultado["segments"]
    
    # Abrimos (o creamos) el archivo .srt para escribir
    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        for i, segmento in enumerate(segmentos, start=1):
            inicio = formato_srt_tiempo(segmento["start"])
            fin = formato_srt_tiempo(segmento["end"])
            texto = segmento["text"].strip()
            
            # Formato estándar de un bloque SRT
            bloque_srt = f"{i}\n{inicio} --> {fin}\n{texto}\n\n"
            archivo.write(bloque_srt)

    # Limpieza: elimina el archivo de audio temporal
    if os.path.exists(ruta_audio_temporal):
        os.remove(ruta_audio_temporal)

    return f"¡Listo! Subtítulos guardados exitosamente en: {archivo_salida}"

# --- Ejecución ---
if __name__ == "__main__":
    # RECUERDA: Cambia el nombre de este archivo por tu video real
    archivo_video = "mi_video.mp4"  
    archivo_subtitulos = "mis_subtitulos.srt" 
    
    if os.path.exists(archivo_video):
        mensaje = video_a_srt(archivo_video, archivo_salida=archivo_subtitulos)
        print("\n" + mensaje)
    else:
        print(f"Error: No se encontró el archivo de video '{archivo_video}'. Asegúrate de que esté en la misma carpeta que este script.")
