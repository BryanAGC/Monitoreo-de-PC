import socket
import struct
import tkinter as tk
from PIL import Image, ImageTk
import io
import threading
import pyautogui
import sys

class ScreenSharingServer:
    def __init__(self, root):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 9998))  # Dirección IP del servidor
        self.server_socket.listen(2)

        self.pc1_socket = None
        self.pc2_socket = None

        self.root = root
        self.root.title("Servidor de Pantalla Remota")

        # Configuración de fondo oscuro para la ventana principal
        self.root.configure(bg="#2E2E2E")

        # Label para mostrar la pantalla en el servidor
        self.label = tk.Label(root, bg="#2E2E2E")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Botones para elegir qué cliente observar
        self.pc1_button = tk.Button(root, text="Observar PC1", command=lambda: self.select_client(self.pc1_socket),
                                    bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.pc1_button.grid(row=1, column=0, padx=10, pady=10)

        self.pc2_button = tk.Button(root, text="Observar PC2", command=lambda: self.select_client(self.pc2_socket),
                                    bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.pc2_button.grid(row=2, column=0, padx=10, pady=10)

        # Hilos
        self.relay_thread = None
        self.send_thread = None
        self.transmission_window = None

        # Variable para controlar si está transmitiendo
        self.transmitting = False

        # Variable para controlar la ejecución del servidor
        self.running = True

    def start(self):
        """Esperar conexiones de los clientes (PC1 y PC2)"""
        try:
            print("Esperando conexión de PC1...")
            self.pc1_socket, pc1_addr = self.server_socket.accept()
            print(f"PC1 conectado desde: {pc1_addr}")

            print("Esperando conexión de PC2...")
            self.pc2_socket, pc2_addr = self.server_socket.accept()
            print(f"PC2 conectado desde: {pc2_addr}")

            # Iniciar el hilo de manejo de comunicaciones
            self.relay_thread = threading.Thread(target=self.handle_communication)
            self.relay_thread.daemon = True  # Hilo en segundo plano
            self.relay_thread.start()

            # Hilo para cerrar todo después de un tiempo si no se detiene manualmente
            self.shutdown_thread = threading.Thread(target=self.shutdown)
            self.shutdown_thread.daemon = True
            self.shutdown_thread.start()

        except OSError as e:
            print(f"Error al aceptar la conexión: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def handle_communication(self):
        """Manejar la transmisión de la pantalla entre PC1 y PC2"""
        while self.running:
            print("Esperando elección de PC1 o PC2 para transmitir o recibir...")
            try:
                # En este caso, los botones en la interfaz del servidor permiten elegir qué PC observar
                # La elección se hace automáticamente sin intervención de los clientes.
                pass
            except Exception as e:
                print(f"Error en la comunicación entre clientes: {e}")
                break

    def select_client(self, selected_socket):
        """Seleccionar el cliente a observar (PC1 o PC2)"""
        self.selected_socket = selected_socket
        self.relay_screen()

    def relay_screen(self):
        """Transmitir la pantalla desde el cliente seleccionado al servidor"""
        try:
            while self.running:
                # Recibir el tamaño del mensaje
                packed_msg_size = self.selected_socket.recv(struct.calcsize("I"))
                if not packed_msg_size:
                    break

                msg_size = struct.unpack("I", packed_msg_size)[0]
                print(f"Reenviando imagen de {msg_size} bytes")

                data = b""
                while len(data) < msg_size:
                    packet = self.selected_socket.recv(min(msg_size - len(data), 4096))
                    if not packet:
                        break
                    data += packet

                # Mostrar la pantalla en el servidor
                self.display_image(data)

        except Exception as e:
            print(f"Error al reenviar o mostrar pantalla: {e}")

    def display_image(self, data):
        """Mostrar la imagen recibida en la interfaz del servidor"""
        try:
            img = Image.open(io.BytesIO(data))
            img_tk = ImageTk.PhotoImage(img)

            self.label.config(image=img_tk)
            self.label.image = img_tk

            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            print(f"Error al cargar o mostrar la imagen en el servidor: {e}")

    def stop_server(self):
        """Detener el servidor y cerrar todas las conexiones"""
        self.running = False  # Detener el ciclo de ejecución
        if self.pc1_socket:
            self.pc1_socket.close()
        if self.pc2_socket:
            self.pc2_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print("Servidor detenido correctamente.")
        sys.exit(0)  # Cerrar el proceso completamente


if __name__ == "__main__":
    root = tk.Tk()
    server = ScreenSharingServer(root)
    threading.Thread(target=server.start, daemon=True).start()
    root.mainloop()
