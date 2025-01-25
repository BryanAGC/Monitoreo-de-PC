import shutil
import os
from tkinter import  messagebox

# Ruta origen de los archivos
ruta_origen = r"C:\Users\hecto\Documents\TESJI\Transfer"
# Ruta destino donde se copiarán los archivos
ruta_destino = r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\servidor\transfer_arch"

def copiar_archivo(nombre_archivo):
    # Formamos la ruta completa del archivo
    archivo_origen = os.path.join(ruta_origen, nombre_archivo)
    archivo_destino = os.path.join(ruta_destino, nombre_archivo)
    
    try:
        if os.path.exists(archivo_origen):
            shutil.copy(archivo_origen, archivo_destino)  # Realiza la copia del archivo
            print(f"Archivo {nombre_archivo} Guardado Correctamente en: {ruta_destino}")
            messagebox.showinfo("Exito", "Archivo Recibido Correctamnte")
        else:
            print(f"Archivo {nombre_archivo} no encontrado en la ruta de origen.")
    except Exception as e:
        print(f"Error al copiar el archivo {nombre_archivo}: {e}")
