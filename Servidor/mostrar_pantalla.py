import socket
import struct
import pyautogui
import threading
import io
import tkinter as tk
from PIL import Image, ImageTk
import sys

class ScreenSharingServer:
    def __init__(self, root):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 9998))  # Dirección IP del servidor
        self.server_socket.listen(2)

        self.clients = []  # Lista de clientes conectados
        self.root = root
        self.root.title("Servidor de Pantalla Remota")

        # Configuración de fondo oscuro para la ventana principal
        self.root.configure(bg="#2E2E2E")

        # Label para mostrar la pantalla en el servidor
        self.label = tk.Label(root, bg="#2E2E2E")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Botón para abrir la ventana de transmisión
        self.send_button = tk.Button(root, text="Iniciar Transmisión", command=self.start_transmitting, 
                                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.send_button.grid(row=1, column=0, padx=10, pady=10)

        # Botón para detener la transmisión
        self.stop_button = tk.Button(root, text="Detener Transmisión", command=self.stop_transmitting, 
                                     bg="#F44336", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.grid(row=2, column=0, padx=10, pady=10)

        # Hilos
        self.transmitting = False
        self.running = True

    def start(self):
        """Esperar conexiones de los clientes"""
        try:
            while self.running:
                print("Esperando conexión de un cliente...")
                client_socket, client_addr = self.server_socket.accept()
                print(f"Cliente conectado desde: {client_addr}")
                self.clients.append(client_socket)

                # Hilo para manejar la comunicación con el cliente
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True  # Hilo en segundo plano
                client_thread.start()

        except OSError as e:
            print(f"Error al aceptar la conexión: {e}")

    def handle_client(self, client_socket):
        """Manejar la comunicación con un cliente específico"""
        while self.running:
            try:
                client_socket.recv(1024)  # Espera hasta recibir algo
            except Exception as e:
                print(f"Error con cliente: {e}")
                break

    def start_transmitting(self):
        """Iniciar la transmisión de la pantalla"""
        if not self.transmitting:
            self.transmitting = True
            self.send_screen_thread = threading.Thread(target=self.send_screen_to_clients)
            self.send_screen_thread.daemon = True  # Hilo en segundo plano
            self.send_screen_thread.start()

    def stop_transmitting(self):
        """Detener la transmisión de la pantalla"""
        self.transmitting = False

    def send_screen_to_clients(self):
        """Capturar y enviar la pantalla del servidor a los clientes"""
        try:
            while self.transmitting and self.running:
                screenshot = pyautogui.screenshot()

                img_byte_array = io.BytesIO()
                screenshot.save(img_byte_array, format='JPEG')
                img_data = img_byte_array.getvalue()

                message_size = struct.pack("I", len(img_data))
                print(f"Enviando pantalla del servidor: {len(img_data)} bytes")

                for client_socket in self.clients:
                    try:
                        client_socket.sendall(message_size + img_data)
                    except Exception as e:
                        print(f"Error al enviar imagen al cliente: {e}")

        except Exception as e:
            print(f"Error al transmitir la pantalla del servidor: {e}")

    def display_image(self, data):
        """Mostrar la imagen en la interfaz del servidor"""
        try:
            img = Image.open(io.BytesIO(data))
            img_tk = ImageTk.PhotoImage(img)

            self.label.config(image=img_tk)
            self.label.image = img_tk

            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            print(f"Error al mostrar la imagen en la interfaz del servidor: {e}")

    def stop_server(self):
        """Detener el servidor y cerrar las conexiones"""
        self.running = False  # Detener el ciclo de ejecución
        for client_socket in self.clients:
            client_socket.close()
        self.server_socket.close()
        print("Servidor detenido correctamente.")
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    server = ScreenSharingServer(root)
    threading.Thread(target=server.start, daemon=True).start()
    root.mainloop()
