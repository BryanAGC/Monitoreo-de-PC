import socket
import struct
import tkinter as tk
from PIL import Image, ImageTk
import io

class ScreenSharingClient:
    def __init__(self, root, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar al servidor
        self.client_socket.connect((self.server_ip, self.server_port))

        self.root = root
        self.root.title("Cliente de Pantalla Remota")
        self.label = tk.Label(root, bg="#2E2E2E")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.root.after(100, self.receive_screen)  # Iniciar la recepción de imágenes

    def receive_screen(self):
        """Recibir la pantalla transmitida desde el servidor y mostrarla"""
        try:
            while True:
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

                self.display_image(data)
        except Exception as e:
            print(f"Error al recibir la pantalla: {e}")

    def display_image(self, data):
        """Mostrar la imagen recibida en la interfaz del cliente"""
        try:
            img = Image.open(io.BytesIO(data))
            img_tk = ImageTk.PhotoImage(img)

            self.label.config(image=img_tk)
            self.label.image = img_tk

            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            print(f"Error al mostrar la imagen en la interfaz del cliente: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    client = ScreenSharingClient(root, "127.0.0.1", 9998)
    root.mainloop()
