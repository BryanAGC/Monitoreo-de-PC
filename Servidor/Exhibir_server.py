import socket
import struct
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

        # Botón para iniciar la transmisión
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

        self.emisor = None  # Cliente emisor
        self.receptor = None  # Cliente receptor

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
        try:
            # Asignar un cliente como emisor y otro como receptor
            if self.emisor is None:
                self.emisor = client_socket
                client_socket.send(b"ROLE:EMISOR")
            elif self.receptor is None:
                self.receptor = client_socket
                client_socket.send(b"ROLE:RECEPTOR")

            # Los clientes deben esperar la orden del servidor
            while self.running:
                client_socket.recv(1024)  # El cliente debe esperar hasta recibir la orden

        except Exception as e:
            print(f"Error con cliente: {e}")
            if client_socket == self.emisor:
                self.emisor = None
            if client_socket == self.receptor:
                self.receptor = None
            self.clients.remove(client_socket)
            client_socket.close()

    def start_transmitting(self):
        """Iniciar la transmisión de la pantalla desde el emisor al receptor"""
        if self.emisor and self.receptor:
            self.transmitting = True
            self.send_screen_thread = threading.Thread(target=self.send_screen_to_receptor)
            self.send_screen_thread.daemon = True  # Hilo en segundo plano
            self.send_screen_thread.start()

            # Enviar la orden a los clientes para comenzar la transmisión
            self.emisor.send(b"START_TRANSMISSION")
            self.receptor.send(b"START_RECEIVING")

    def stop_transmitting(self):
        """Detener la transmisión de la pantalla"""
        self.transmitting = False
        self.emisor.send(b"STOP_TRANSMISSION")
        self.receptor.send(b"STOP_RECEIVING")

    def send_screen_to_receptor(self):
        """Capturar y enviar la pantalla del emisor al receptor"""
        try:
            while self.transmitting and self.running:
                screenshot = self.receive_screen_from_emisor()

                img_byte_array = io.BytesIO()
                screenshot.save(img_byte_array, format='JPEG')
                img_data = img_byte_array.getvalue()

                message_size = struct.pack("I", len(img_data))
                print(f"Enviando pantalla del emisor al receptor: {len(img_data)} bytes")

                self.receptor.sendall(message_size + img_data)

        except Exception as e:
            print(f"Error al transmitir la pantalla del emisor: {e}")

    def receive_screen_from_emisor(self):
        """Recibir la pantalla del emisor"""
        try:
            msg_size = self.emisor.recv(4)
            msg_size = struct.unpack("I", msg_size)[0]
            data = self.emisor.recv(msg_size)
            return Image.open(io.BytesIO(data))
        except Exception as e:
            print(f"Error al recibir la pantalla del emisor: {e}")
            return None

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
