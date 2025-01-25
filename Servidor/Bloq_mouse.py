# Bloq_mouse.py
def enviar_comando(cliente_socket, comando):
    """
    Función para enviar comandos de bloqueo o desbloqueo al cliente.
    """
    cliente_socket.send(comando.encode("utf-8"))
