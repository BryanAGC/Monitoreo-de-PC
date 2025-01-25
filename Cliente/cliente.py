import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import os
import time
import random
import transferencia_cliente
import bloqmause
import bloquear_paginas

# Configuración del cliente
SERVER_IP = '192.168.1.65'
SERVER_PORT = 8080
PING_COUNT = 4
ping_active = False
ping_attempt = 0

# Lista de archivos permitidos
archivos_permitidos = ["Fondo1.jpg", "Fondo2.jpg", "Fondo3.jpg", "Fondo4.jpg", "Archivo_transferencia.txt"]

# Configurar el socket del cliente
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Función para intentar la conexión al servidor
def conectar_servidor():
    try:
        cliente_socket.connect((SERVER_IP, SERVER_PORT))
        estado_conexion.config(text="Conectado", fg="green")
        boton_conectar.config(state=tk.DISABLED)
        threading.Thread(target=escuchar_servidor, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")

# Función para escuchar mensajes del servidor
def escuchar_servidor():
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode("utf-8")
            procesar_mensaje(mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error: {e}")
            break

# Función para procesar mensajes del servidor
def procesar_mensaje(mensaje):
    if mensaje == "bloquear":
        bloqmause.gestionar_bloqueo("bloquear")
    elif mensaje == "desbloquear":
        bloqmause.gestionar_bloqueo("desbloquear")
    elif mensaje == "bloquear_paginas":
        bloquear_paginas.gestionar_bloqueo_paginas("bloquear")
    elif mensaje == "desbloquear_paginas":
        bloquear_paginas.gestionar_bloqueo_paginas("desbloquear")
    elif mensaje == "Iniciar Chat":
        abrir_chat()
    elif mensaje == "Apagar PC":
        manejar_apagado()
    elif mensaje.startswith("Archivo transferido: "):
        # Extrae el nombre del archivo del mensaje
        nombre_archivo = mensaje.split(": ")[-1].strip()
        if nombre_archivo in archivos_permitidos:
            # Llama a la función copiar_archivo en transferencia_cliente
            try:
                transferencia_cliente.copiar_archivo(nombre_archivo)
                messagebox.showinfo("Éxito", f"{nombre_archivo} recibido correctamente.")
            except FileNotFoundError as e:
                messagebox.showerror("Error", str(e))
        else:
            area_chat.insert(tk.END, f"Archivo {nombre_archivo} no permitido para transferencia.\n")
            area_chat.see(tk.END)
    elif 'ventana_chat' in globals():
        area_chat.insert(tk.END, f"Servidor: {mensaje}\n")
        area_chat.see(tk.END)



# Función para enviar pings al servidor
def enviar_ping():
    global ping_active, ping_attempt
    ping_active = True
    ventana_ping = tk.Toplevel()
    ventana_ping.title("Resultados de Ping")
    ventana_ping.geometry("400x300")
    area_ping = scrolledtext.ScrolledText(ventana_ping, wrap=tk.WORD)
    area_ping.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    area_ping.config(state=tk.NORMAL)

    paquetes_enviados = 0
    paquetes_recibidos = 0
    tiempos_respuesta = []

    if ping_attempt % 2 == 1:
        area_ping.insert(tk.END, "No se puede enviar Ping al host destino\n")
    else:
        area_ping.insert(tk.END, f"Haciendo ping a {SERVER_IP} con 32 bytes de datos:\n")
        
        def simular_ping(indice):
            nonlocal paquetes_enviados, paquetes_recibidos
            if indice < PING_COUNT:
                time.sleep(0.5)
                paquetes_enviados += 1
                tiempo = random.randint(1, 500)
                area_ping.insert(tk.END, f"Respuesta desde {SERVER_IP}: bytes=32 tiempo={tiempo}ms TTL=128\n")
                tiempos_respuesta.append(tiempo)
                paquetes_recibidos += 1
                ventana_ping.after(1000, simular_ping, indice + 1)
            else:
                area_ping.insert(tk.END, f"\nEstadísticas de ping para {SERVER_IP}:\n")
                area_ping.insert(tk.END, f"Paquetes: enviados = {paquetes_enviados}, recibidos = {paquetes_recibidos}, perdidos = {paquetes_enviados - paquetes_recibidos}\n")
                porcentaje_perdidos = (paquetes_enviados - paquetes_recibidos) / paquetes_enviados * 100
                area_ping.insert(tk.END, f"({porcentaje_perdidos:.0f}% perdidos)\n")
                if tiempos_respuesta:
                    area_ping.insert(tk.END, f"Mínimo = {min(tiempos_respuesta)}ms, Máximo = {max(tiempos_respuesta)}ms, Media = {sum(tiempos_respuesta) // len(tiempos_respuesta)}ms\n")
        simular_ping(0)

    ping_attempt += 1
    ping_active = False

# Función para manejar el apagado de la PC con cuenta regresiva
def manejar_apagado():
    ventana_apagado = tk.Toplevel()
    ventana_apagado.title("Apagado en Progreso")
    ventana_apagado.geometry("300x100")
    etiqueta_tiempo = tk.Label(ventana_apagado, text="La PC se apagará en 5 segundos", font=("Arial", 12))
    etiqueta_tiempo.pack(pady=20)

    def cuenta_regresiva(tiempo):
        if tiempo > 0:
            etiqueta_tiempo.config(text=f"La PC se apagará en {tiempo} segundo(s)")
            ventana_apagado.after(1000, cuenta_regresiva, tiempo - 1)
        else:
            ventana_apagado.destroy()
            os.system("shutdown /s /t 1")

    cuenta_regresiva(5)

# Función para abrir la interfaz de chat
def abrir_chat():
    global ventana_chat, area_chat, entrada_mensaje
    ventana_chat = tk.Toplevel()
    ventana_chat.title("Chat con Servidor")
    ventana_chat.geometry("400x400")

    area_chat = scrolledtext.ScrolledText(ventana_chat, wrap=tk.WORD)
    area_chat.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    area_chat.config(state=tk.NORMAL)

    entrada_mensaje = tk.Entry(ventana_chat, width=50)
    entrada_mensaje.pack(pady=5)

    boton_enviar = tk.Button(ventana_chat, text="Enviar", command=enviar_mensaje)
    boton_enviar.pack()
    boton_seleccionar_archivo = tk.Button(ventana_chat, text="Enviar Archivo", command=seleccionar_y_enviar_archivo)
    boton_seleccionar_archivo.pack()

# Función para enviar mensajes al servidor
def enviar_mensaje():
    mensaje = entrada_mensaje.get()
    if mensaje:
        cliente_socket.send(mensaje.encode("utf-8"))
        area_chat.insert(tk.END, f"Tú: {mensaje}\n")
        area_chat.see(tk.END)
        entrada_mensaje.delete(0, tk.END)

# Función para seleccionar y enviar archivo
def seleccionar_y_enviar_archivo():
    archivo_seleccionado = filedialog.askopenfilename()
    if archivo_seleccionado:
        nombre_archivo = os.path.basename(archivo_seleccionado)
        cliente_socket.send(f"Archivo transferido: {nombre_archivo}".encode("utf-8"))
        area_chat.insert(tk.END, f"Tú: Archivo enviado - {nombre_archivo}\n")
        area_chat.see(tk.END)
        messagebox.showinfo("Éxito", "Archivo enviado correctamente al servidor")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Cliente - MonitorPC")
ventana.geometry("300x250")
ventana.configure(bg="#e6e6e6")  # Color de fondo claro para la ventana

# Etiqueta de estado de conexión con color más claro y estilo profesional
estado_conexion = tk.Label(
    ventana,
    text="Desconectado",
    fg="#5a5a5a",  # Color de texto gris oscuro
    bg="#d3d3d3",  # Color de fondo gris claro para la etiqueta de estado
    font=("Arial", 12, "bold"),
    width=20,
    pady=5
)
estado_conexion.pack(pady=10)

# Estilo uniforme para los botones con colores diferenciados
boton_conectar = tk.Button(
    ventana,
    text="Conectar al Servidor",
    command=conectar_servidor,
    bg="#4CAF50",   # Verde suave
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,
    height=2
)
boton_conectar.pack(pady=5)

boton_ping = tk.Button(
    ventana,
    text="Enviar Ping",
    command=enviar_ping,
    bg="#2196F3",   # Azul suave
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,
    height=2
)
boton_ping.pack(pady=5)


ventana.mainloop()