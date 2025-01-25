import socket
import struct
import pyautogui
import io
import threading
import tkinter as tk
from PIL import Image, ImageTk

class ScreenSharingClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

        # No queremos que haya una interfaz gráfica visible hasta que el servidor lo ordene
        self.root = tk.Tk()
        self.root.withdraw()  # Esconde la ventana inicial

        self.label = tk.Label(self.root)
        self.label.grid(row=0, column=0)

        # Hilos
        self.receive_thread = None
        self.send_thread = None

        self.running = True

    def start(self):
        """Iniciar la comunicación con el servidor."""
        try:
            # Hilo para recibir la pantalla del servidor
            self.receive_thread = threading.Thread(target=self.receive_screen)
            self.receive_thread.daemon = True  # Hilo en segundo plano
            self.receive_thread.start()

            # Hilo para enviar la pantalla del cliente al servidor
            self.send_thread = threading.Thread(target=self.send_screen)
            self.send_thread.daemon = True  # Hilo en segundo plano
            self.send_thread.start()

        except Exception as e:
            print(f"Error en la comunicación con el servidor: {e}")

    def receive_screen(self):
        """Recibir la pantalla del servidor y mostrarla en el cliente."""
        try:
            while self.running:
                # Escuchar el comando del servidor para mostrar una imagen
                command = self.client_socket.recv(1024).decode()

                if command == "mostrar_imagen":
                    # Recibir el tamaño del mensaje
                    packed_msg_size = self.client_socket.recv(struct.calcsize("I"))
                    if not packed_msg_size:
                        break

                    msg_size = struct.unpack("I", packed_msg_size)[0]
                    data = b""
                    while len(data) < msg_size:
                        packet = self.client_socket.recv(min(msg_size - len(data), 4096))
                        if not packet:
                            break
                        data += packet

                    # Mostrar la imagen recibida en la interfaz del cliente
                    self.display_image(data)

        except Exception as e:
            print(f"Error al recibir o mostrar la pantalla: {e}")

    def send_screen(self):
        """Capturar la pantalla del cliente y enviarla al servidor."""
        try:
            while self.running:
                # Capturar la pantalla del cliente
                screenshot = pyautogui.screenshot()

                # Convertir la imagen a bytes
                img_byte_array = io.BytesIO()
                screenshot.save(img_byte_array, format='JPEG')
                img_data = img_byte_array.getvalue()

                # Enviar los datos de la imagen al servidor
                message_size = struct.pack("I", len(img_data))
                self.client_socket.sendall(message_size + img_data)

        except Exception as e:
            print(f"Error al capturar y enviar la pantalla: {e}")

    def display_image(self, data):
        """Mostrar la imagen recibida en la interfaz del cliente."""
        try:
            img = Image.open(io.BytesIO(data))
            img_tk = ImageTk.PhotoImage(img)

            # Hacer visible la ventana cuando el servidor ordene mostrar la imagen
            self.root.deiconify()  # Mostrar la ventana
            self.label.config(image=img_tk)
            self.label.image = img_tk

            self.root.update_idletasks()
            self.root.update()

        except Exception as e:
            print(f"Error al cargar o mostrar la imagen en el cliente: {e}")

    def stop(self):
        """Detener la ejecución del cliente."""
        self.running = False
        self.client_socket.close()
        print("Cliente detenido.")

if __name__ == "__main__":
    # Configura la IP y el puerto del servidor
    server_ip = '192.168.1.100'  # Cambia por la IP del servidor
    server_port = 9998
    client = ScreenSharingClient(server_ip, server_port)
    client.start()
    client.root.mainloop()
