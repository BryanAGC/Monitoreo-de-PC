import keyboard
import threading
import pyautogui
import time

# Lista de teclas comunes a bloquear, incluyendo la letra 'ñ' y otros caracteres especiales
teclas = [
    'esc', 'enter', 'shift', 'ctrl', 'alt', 'tab', 'backspace', 'space',
    'up', 'down', 'left', 'right', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'ñ', '.', ',', '¿', '?', '¡', "'", '{', '}', '[', ']', '(', ')', '#', '&', '+', '-', '*', '/', '"', '^', '´'
]

mouse_bloqueado = False

# Función para bloquear el teclado
def bloquear_teclado():
    print("Teclado bloqueado.")
    for tecla in teclas:
        keyboard.block_key(tecla)

# Función para desbloquear el teclado
def desbloquear_teclado():
    print("Teclado desbloqueado.")
    for tecla in teclas:
        keyboard.unblock_key(tecla)

# Función para fijar la posición del puntero del mouse, bloqueando el movimiento completamente
def bloquear_mouse():
    print("Mouse bloqueado.")
    global mouse_bloqueado
    mouse_bloqueado = True
    # Obtener la posición inicial del mouse
    x, y = pyautogui.position()
    # Bloquear el movimiento del mouse mientras el bloqueo esté activado
    while mouse_bloqueado:
        # Fijar el mouse en su posición inicial
        pyautogui.moveTo(x, y)
        time.sleep(0.01)  # Evita uso excesivo de CPU

# Función para desbloquear el movimiento del mouse
def desbloquear_mouse():
    global mouse_bloqueado
    mouse_bloqueado = False
    print("Mouse desbloqueado.")

# Función principal para gestionar el bloqueo o desbloqueo
def gestionar_bloqueo(accion):
    if accion == "bloquear":
        threading.Thread(target=bloquear_teclado).start()
        threading.Thread(target=bloquear_mouse).start()
    elif accion == "desbloquear":
        desbloquear_teclado()
        desbloquear_mouse()
