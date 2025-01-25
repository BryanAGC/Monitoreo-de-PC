import os
import shutil

# Directorio origen donde se encuentran los archivos permitidos
directorio_origen = r"C:\Users\hecto\OneDrive\Pictures\trans"

def copiar_archivo(nombre_archivo):
    ruta_origen = os.path.join(directorio_origen, nombre_archivo)
    ruta_guardado = r"C:\Users\hecto\OneDrive\Documents\MonitorPC\cliente\transfer"
    
    # Crea la carpeta de destino si no existe
    os.makedirs(ruta_guardado, exist_ok=True)
    ruta_destino = os.path.join(ruta_guardado, nombre_archivo)

    # Verifica si el archivo existe en el directorio origen antes de copiarlo
    if os.path.exists(ruta_origen):
        shutil.copy(ruta_origen, ruta_destino)
    else:
        raise FileNotFoundError(f"El archivo {nombre_archivo} no existe en el directorio origen.")
