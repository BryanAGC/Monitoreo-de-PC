import os
import sys
import ctypes

# Lista de URLs que se desea bloquear
URLS_BLOQUEADAS = [
    "youtube.com", "www.youtube.com",
    "amazon.com.mx", "www.amazon.com.mx",
    "mercadolibre.com.mx", "www.mercadolibre.com.mx"
]

# Ruta del archivo de hosts en el sistema
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECCION = "127.0.0.1"  # IP a la que se redireccionan las URLs bloqueadas

def ejecutar_como_administrador():
    """Intenta ejecutar el script con permisos de administrador."""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Reintentar el script con permisos elevados
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return False

# Función para gestionar el bloqueo o desbloqueo de páginas web
def gestionar_bloqueo_paginas(accion):
    try:
        # Intentar obtener permisos de administrador
        if not ejecutar_como_administrador():
            return

        # Leer contenido actual del archivo de hosts
        with open(HOSTS_PATH, 'r') as archivo:
            lineas = archivo.readlines()

        # Modificar el archivo hosts según la acción (bloquear o desbloquear)
        if accion == "bloquear":
            with open(HOSTS_PATH, 'w') as archivo:
                for linea in lineas:
                    if not any(url in linea for url in URLS_BLOQUEADAS):
                        archivo.write(linea)
                for url in URLS_BLOQUEADAS:
                    archivo.write(f"{REDIRECCION} {url}\n")
            print("Páginas bloqueadas exitosamente.")

        elif accion == "desbloquear":
            with open(HOSTS_PATH, 'w') as archivo:
                for linea in lineas:
                    if not any(url in linea for url in URLS_BLOQUEADAS):
                        archivo.write(linea)
            print("Páginas desbloqueadas exitosamente.")

        else:
            print("Acción no reconocida. Use 'bloquear' o 'desbloquear'.")

    except PermissionError as e:
        print(f"Error de permisos: {e}")
    except Exception as e:
        print(f"Error: {e}")