import socket
import subprocess

# Configuración del servidor
SERVER_HOST = "127.0.0.1"  # Cambiar por la dirección IP del servidor si no está en localhost
SERVER_PORT = 65432        # Puerto del servidor

# Rutas de los scripts
RUTA_VER_CLIENTE = r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\cliente\mostrar_pantalla.py"
RUTA_MOSTRAR_SERVIDOR = r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\cliente\ver_pantalla.py"
RUTA_EXHIBIR_CLIENTE = r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\cliente\Exhibir_cliente.py"

def conectar_al_servidor():
    """Establece conexión con el servidor y escucha comandos."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((SERVER_HOST, SERVER_PORT))
            print(f"Conectado al servidor en {SERVER_HOST}:{SERVER_PORT}")

            while True:
                # Recibir mensajes del servidor
                mensaje = cliente.recv(1024).decode("utf-8")
                if not mensaje:
                    print("Conexión cerrada por el servidor.")
                    break

                print(f"Mensaje recibido: {mensaje}")
                
                # Procesar mensajes y ejecutar el archivo correspondiente
                if mensaje == "ver_cliente":
                    print("Ejecutando mostrar_pantalla.py...")
                    subprocess.Popen(["python", RUTA_VER_CLIENTE])
                elif mensaje == "mostrar_servidor":
                    print("Ejecutando ver_pantalla.py...")
                    subprocess.Popen(["python", RUTA_MOSTRAR_SERVIDOR])
                elif mensaje == "exhibir":
                    print("Ejecutando Exhibir_cliente.py...")
                    subprocess.Popen(["python", RUTA_EXHIBIR_CLIENTE])
                else:
                    print(f"Comando no reconocido: {mensaje}")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verifique que el servidor esté activo.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    conectar_al_servidor()
