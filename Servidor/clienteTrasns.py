import socket
import struct
import io
import pyautogui


class ScreenSharingClient:
    def __init__(self, server_ip):
        """Inicializa la conexión con el servidor."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, 9998))  # Conectar al servidor
            print("Conexión exitosa al servidor.")
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            raise

    def send_screen(self):
        """Enviar la pantalla del cliente al servidor."""
        try:
            while True:
                # Capturar pantalla
                screenshot = pyautogui.screenshot()
                img_byte_array = io.BytesIO()
                screenshot.save(img_byte_array, format='JPEG')
                img_data = img_byte_array.getvalue()

                # Empaquetar y enviar tamaño y datos de la imagen
                message_size = struct.pack("I", len(img_data))
                self.client_socket.sendall(message_size + img_data)

        except Exception as e:
            print(f"Error al enviar pantalla: {e}")
        finally:
            self.close()

    def close(self):
        """Cerrar la conexión con el servidor."""
        try:
            self.client_socket.close()
            print("Conexión cerrada.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")


if __name__ == "__main__":
    server_ip = "172.168.2.146"  # Dirección IP del servidor
    client = ScreenSharingClient(server_ip)

    # Enviar pantalla automáticamente
    client.send_screen()
