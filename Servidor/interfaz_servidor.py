import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Label
from tkinter import ttk
from PIL import Image, ImageTk
from Bloq_mouse import enviar_comando  # Importamos la función de bloqueo/desbloqueo
import pantalla_servidor
from transferencia import copiar_archivo  # Importamos la función de copia de archivo


# Configuración del servidor
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8080
clientes = {}
nombres_clientes = {}
ping_permitido_clientes = {}  # Estado inicial para permitir pings individualmente por cliente

# Crear y configurar el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)
print(f"Servidor escuchando en {SERVER_IP}:{SERVER_PORT}")

# Ruta absoluta de la imagen
IMG_PATH = r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\servidor\images.png"

# Función para aceptar nuevas conexiones de clientes
def aceptar_clientes():
    contador_cliente = 1
    while True:
        cliente_socket, direccion = server_socket.accept()
        nombre_cliente = f"Cliente {contador_cliente}"
        clientes[nombre_cliente] = cliente_socket
        nombres_clientes[direccion] = nombre_cliente
        ping_permitido_clientes[nombre_cliente] = True  # Ping permitido por defecto para cada cliente
        contador_cliente += 1
        actualizar_lista_clientes()
        threading.Thread(target=recibir_mensajes_cliente, args=(cliente_socket, nombre_cliente)).start()

# Lista de archivos permitidos para la transferencia
archivos_permitidos = ["archivo1.txt", "alien-removebg-preview.png", "nave-removebg-preview.png"]

# Función para recibir mensajes de los clientes
def recibir_mensajes_cliente(cliente_socket, nombre_cliente):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode("utf-8")
            if mensaje.startswith("Archivo transferido:"):
                # Extraemos el nombre del archivo desde el mensaje
                nombre_archivo = mensaje.replace("Archivo transferido: ", "").strip()
                
                # Verificamos si el archivo está en la lista de archivos permitidos
                if nombre_archivo in archivos_permitidos:
                    # Si es válido, llamamos a la función para copiar el archivo
                    copiar_archivo(nombre_archivo)
                else:
                    print(f"Archivo {nombre_archivo} no está permitido para transferencia.")
            elif mensaje:
                if nombre_cliente in ventanas_chat:
                    area_chat = ventanas_chat[nombre_cliente]["area_chat"]
                    area_chat.insert(tk.END, f"{nombre_cliente}: {mensaje}\n")
                    area_chat.see(tk.END)
        except Exception as e:
            print(f"Error al recibir mensaje de {nombre_cliente}: {e}")
            cliente_socket.close()
            del clientes[nombre_cliente]
            del ping_permitido_clientes[nombre_cliente]
            actualizar_lista_clientes()
            break

# Función para actualizar la lista de clientes en la interfaz
def actualizar_lista_clientes():
    for row in treeview.get_children():
        treeview.delete(row)
    
    for nombre_cliente in clientes.keys():
        # Añadir icono encima del nombre del cliente
        treeview.insert("", "end", text=nombre_cliente, image=img_icono)

# Diccionario para almacenar ventanas de chat abiertas
ventanas_chat = {}

# Función para iniciar el chat con el cliente seleccionado
def iniciar_chat():
    seleccion = treeview.selection()
    if seleccion:
        nombre_cliente = treeview.item(seleccion)["text"]
        cliente_socket = clientes[nombre_cliente]
        cliente_socket.send("Iniciar Chat".encode("utf-8"))
        
        ventana_chat = tk.Toplevel()
        ventana_chat.title(f"Chat con {nombre_cliente}")
        ventana_chat.geometry("400x400")

        area_chat = scrolledtext.ScrolledText(ventana_chat, wrap=tk.WORD)
        area_chat.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        area_chat.config(state=tk.NORMAL)

        entrada_mensaje = tk.Entry(ventana_chat, width=50)
        entrada_mensaje.pack(pady=5)

        boton_enviar = tk.Button(ventana_chat, text="Enviar", command=lambda: enviar_mensaje(cliente_socket, area_chat, entrada_mensaje))
        boton_enviar.pack()

        # Botón para seleccionar archivo y enviar nombre
        boton_seleccionar_archivo = tk.Button(ventana_chat, text="Enviar Archivo", command=lambda: seleccionar_y_enviar_archivo(cliente_socket, area_chat))
        boton_seleccionar_archivo.pack()

        ventanas_chat[nombre_cliente] = {"ventana": ventana_chat, "area_chat": area_chat}
        threading.Thread(target=recibir_mensajes_chat, args=(cliente_socket, area_chat), daemon=True).start()

# Función para enviar mensajes al cliente desde el servidor
def enviar_mensaje(cliente_socket, area_chat, entrada_mensaje):
    mensaje = entrada_mensaje.get()
    if mensaje:
        cliente_socket.send(mensaje.encode("utf-8"))
        area_chat.insert(tk.END, f"Tú: {mensaje}\n")
        area_chat.see(tk.END)
        entrada_mensaje.delete(0, tk.END)

# Función para seleccionar un archivo y enviar su nombre al cliente
def seleccionar_y_enviar_archivo(cliente_socket, area_chat):
    archivo_seleccionado = filedialog.askopenfilename()  # Abre el explorador de archivos
    if archivo_seleccionado:
        nombre_archivo = archivo_seleccionado.split('/')[-1]  # Extrae solo el nombre del archivo
        cliente_socket.send(f"Archivo transferido: {nombre_archivo}".encode("utf-8"))
        area_chat.insert(tk.END, f"Tú: Archivo enviado - {nombre_archivo}\n")
        area_chat.see(tk.END)
        
        # Mostrar mensaje emergente de confirmación
        messagebox.showinfo("Éxito", "Archivo enviado correctamente al cliente")

# Función para recibir mensajes en la ventana de chat
def recibir_mensajes_chat(cliente_socket, area_chat):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode("utf-8")
            if mensaje:
                area_chat.insert(tk.END, f"Cliente: {mensaje}\n")
                area_chat.see(tk.END)
        except:
            break


# Función para apagar el cliente seleccionado
def apagar_cliente():
    seleccion = treeview.selection()
    if seleccion:
        nombre_cliente = treeview.item(seleccion)["text"]
        cliente_socket = clientes[nombre_cliente]
        cliente_socket.send("Apagar PC".encode("utf-8"))
        messagebox.showinfo("Comando Enviado", f"Se ha enviado el comando de apagado a {nombre_cliente}")

# Función para alternar el permiso de ping de un cliente específico
def toggle_ping_cliente():
    seleccion = treeview.selection()
    if seleccion:
        nombre_cliente = treeview.item(seleccion)["text"]
        ping_permitido_clientes[nombre_cliente] = not ping_permitido_clientes.get(nombre_cliente, True)
        actualizar_lista_clientes()
        estado_ping = "Permitido" if ping_permitido_clientes[nombre_cliente] else "Denegado"
        messagebox.showinfo("Estado de Ping", f"Ping para {nombre_cliente} ha sido {estado_ping}")



# Función para mostrar la imagen en una ventana
def mostrar_imagen(ventana, ruta_imagen):
    imagen = Image.open(ruta_imagen)
    imagen.thumbnail((250, 250))
    imagen_tk = ImageTk.PhotoImage(imagen)
    
    etiqueta_imagen = Label(ventana, image=imagen_tk)
    etiqueta_imagen.image = imagen_tk
    etiqueta_imagen.pack(pady=10)

# Funciones de bloqueo/desbloqueo de teclado y mouse
def bloquear_teclado_mouse():
    seleccion = treeview.selection()
    if seleccion:
        nombre_cliente = treeview.item(seleccion)["text"]
        cliente_socket = clientes[nombre_cliente]
        enviar_comando(cliente_socket, 'bloquear')

def desbloquear_teclado_mouse():
    seleccion = treeview.selection()
    if seleccion:
        nombre_cliente = treeview.item(seleccion)["text"]
        cliente_socket = clientes[nombre_cliente]
        enviar_comando(cliente_socket, 'desbloquear')

# Función para enviar el comando de bloqueo/desbloqueo
def enviar_comando_bloqueo(comando):
    seleccion = treeview.selection()
    if seleccion:
        nombre_cliente = treeview.item(seleccion)["text"]
        cliente_socket = clientes[nombre_cliente]
        cliente_socket.send(comando.encode("utf-8"))

# Configuración de la interfaz gráfica del servidor
ventana_servidor = tk.Tk()
ventana_servidor.title("Servidor")
ventana_servidor.geometry("800x500")  # Aumentamos el ancho para dar espacio a los elementos

etiqueta_clientes = tk.Label(ventana_servidor, text="Clientes conectados", font=("Arial", 14))
etiqueta_clientes.grid(row=0, column=0, columnspan=4, pady=5, sticky="nsew")

# Crear el Treeview que abarca toda la pantalla horizontalmente
treeview = ttk.Treeview(ventana_servidor, columns=("Clientes"), show="tree")
treeview.grid(row=1, column=0, columnspan=4, pady=5, padx=5, sticky="nsew")

# Configuración para que el Treeview se ajuste al ancho completo
ventana_servidor.grid_columnconfigure(0, weight=1)
ventana_servidor.grid_columnconfigure(1, weight=1)
ventana_servidor.grid_columnconfigure(2, weight=1)
ventana_servidor.grid_columnconfigure(3, weight=1)
ventana_servidor.grid_rowconfigure(1, weight=1)

# Crear y configurar la imagen solo después de inicializar la ventana principal
img_icono = Image.open(IMG_PATH)
img_icono = img_icono.resize((50, 50), Image.LANCZOS)
img_icono = ImageTk.PhotoImage(img_icono)

# Tamaño estándar de botones
ancho_boton = 30
alto_boton = 2


# Botones con colores personalizados
boton_iniciar_chat = tk.Button(ventana_servidor, text="Iniciar Chat", command=iniciar_chat, width=ancho_boton, height=alto_boton, bg="#87CEFA")  # Celeste
boton_iniciar_chat.grid(row=2, column=0, pady=5, padx=5)

boton_apagar_cliente = tk.Button(ventana_servidor, text="Apagar Cliente", command=apagar_cliente, width=ancho_boton, height=alto_boton, bg="#FFA500")  # Naranja
boton_apagar_cliente.grid(row=2, column=1, pady=5, padx=5)

boton_ping_cliente = tk.Button(ventana_servidor, text="Alternar Ping Cliente", command=toggle_ping_cliente, width=ancho_boton, height=alto_boton, bg="#32CD32")  # Verde
boton_ping_cliente.grid(row=2, column=2, pady=5, padx=5)

# Nuevo botón para salir
boton_salir = tk.Button(ventana_servidor, text="Salir", command=ventana_servidor.quit, width=ancho_boton, height=alto_boton, bg="#FF5733")  # Rojo
boton_salir.grid(row=2, column=3, pady=5, padx=5)


boton_bloquear = tk.Button(ventana_servidor, text="Bloquear Teclado y Mouse", command=bloquear_teclado_mouse, width=ancho_boton, height=alto_boton, bg="#9370DB")  # Morado
boton_bloquear.grid(row=3, column=0, pady=5, padx=5)

boton_desbloquear = tk.Button(ventana_servidor, text="Desbloquear Teclado y Mouse", command=desbloquear_teclado_mouse, width=ancho_boton, height=alto_boton, bg="#9370DB")  # Morado
boton_desbloquear.grid(row=3, column=1, pady=5, padx=5)

boton_bloquear_web = tk.Button(ventana_servidor, text="Bloquear Páginas Web", command=lambda: enviar_comando_bloqueo("bloquear_paginas"), width=ancho_boton, height=alto_boton, bg="#FFD700")  # Amarillo
boton_bloquear_web.grid(row=3, column=2, pady=5, padx=5)

boton_desbloquear_web = tk.Button(ventana_servidor, text="Desbloquear Páginas Web", command=lambda: enviar_comando_bloqueo("desbloquear_paginas"), width=ancho_boton, height=alto_boton, bg="#FFD700")  # Amarillo
boton_desbloquear_web.grid(row=3, column=3, pady=5, padx=5)

# Hilo para aceptar clientes de forma continua
threading.Thread(target=aceptar_clientes, daemon=True).start()

ventana_servidor.mainloop()

