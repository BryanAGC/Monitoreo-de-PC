import socket
import pyautogui
import struct
from PIL import Image
import io
import time  # Importa la biblioteca para usar time.sleep()

def capture_and_send_screen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9998))
    server_socket.listen(1)
    print("Esperando conexión del cliente...")

    client_socket, addr = server_socket.accept()
    print(f"Conectado con {addr}")

    try:
        while True:
            screenshot = pyautogui.screenshot()

            # Convertir a JPEG
            img_byte_array = io.BytesIO()
            screenshot.save(img_byte_array, format='JPEG')
            img_data = img_byte_array.getvalue()

            # Enviar el tamaño de la imagen usando 4 bytes ('I')
            message_size = struct.pack("I", len(img_data))
            print(f"Enviando tamaño: {len(img_data)} bytes")
            client_socket.sendall(message_size + img_data)

            # Añadir un retraso de 1 segundo entre capturas de pantalla
            time.sleep(0.0001)  # Cambia el valor para ajustar la frecuencia de actualización (1 segundo en este caso)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    capture_and_send_screen()