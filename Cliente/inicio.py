import tkinter as tk
import subprocess
import psutil

class ZAMTronixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZAMTronix")
        self.root.geometry("400x500")  # Ajusté el tamaño para acomodar más botones
        self.root.configure(bg="#2e2e2e")  # Fondo oscuro

        # Etiqueta de bienvenida
        self.label = tk.Label(
            root, 
            text="Bienvenido a ZAMTronix", 
            font=("Arial", 20, "bold"), 
            fg="white", 
            bg="#2e2e2e"
        )
        self.label.pack(pady=30)

        # Sección: Control Remoto
        self.control_remote_frame = tk.Frame(
            root, 
            bd=2, 
            relief="solid", 
            padx=10, pady=10, 
            highlightbackground="#ADD8E6",  # Azul claro
            highlightthickness=2,  # Grosor del contorno
            bg="#2e2e2e"
        )
        self.control_remote_frame.pack(pady=10, padx=10, fill="x")

        self.control_remote_label = tk.Label(
            self.control_remote_frame, 
            text="CONTROL REMOTO", 
            font=("Arial", 16, "bold"), 
            fg="white", 
            bg="#2e2e2e"
        )
        self.control_remote_label.pack(pady=5)

        # Botón de funciones principales
        self.main_functions_button = tk.Button(
            self.control_remote_frame, 
            text="FUNCIONES PRINCIPALES", 
            command=self.open_main_functions, 
            font=("Arial", 14, "bold"), 
            bg="#4CAF50",  # Verde
            fg="white", 
            width=20
        )
        self.main_functions_button.pack(pady=10)

        # Sección: Tipos de Acceso
        self.access_type_frame = tk.Frame(
            root, 
            bd=2, 
            relief="solid", 
            padx=10, pady=10, 
            highlightbackground="#ADD8E6",  # Azul claro
            highlightthickness=2,  # Grosor del contorno
            bg="#2e2e2e"
        )
        self.access_type_frame.pack(pady=10, padx=10, fill="x")

        self.access_type_label = tk.Label(
            self.access_type_frame, 
            text="TIPOS DE ACCESO", 
            font=("Arial", 16, "bold"), 
            fg="white", 
            bg="#2e2e2e"
        )
        self.access_type_label.pack(pady=5)

        # Botón "Acceso 1"
        self.access1_button = tk.Button(
            self.access_type_frame, 
            text="Acceso 1", 
            command=self.access1, 
            font=("Arial", 14, "bold"), 
            bg="#2196F3",  # Azul
            fg="white", 
            width=20
        )
        self.access1_button.pack(pady=10)

        # Botón "Acceso 2"
        self.access2_button = tk.Button(
            self.access_type_frame, 
            text="Acceso 2", 
            command=self.access2, 
            font=("Arial", 14, "bold"), 
            bg="#FFA500",  # Naranja
            fg="white", 
            width=20
        )
        self.access2_button.pack(pady=10)

        # Botón "Acceso 3"
        self.access3_button = tk.Button(
            self.access_type_frame, 
            text="Acceso 3", 
            command=self.access3, 
            font=("Arial", 14, "bold"), 
            bg="#9C27B0",  # Morado
            fg="white", 
            width=20
        )
        self.access3_button.pack(pady=10)

        # Sección: Salir y Finalizar
        self.exit_section_frame = tk.Frame(
            root, 
            bd=2, 
            relief="solid", 
            padx=10, pady=10, 
            highlightbackground="#ADD8E6",  # Azul claro
            highlightthickness=2,  # Grosor del contorno
            bg="#2e2e2e"
        )
        self.exit_section_frame.pack(pady=10, padx=10, fill="x")

        self.exit_section_label = tk.Label(
            self.exit_section_frame, 
            text="FINALIZAR PROCESOS", 
            font=("Arial", 16, "bold"), 
            fg="white", 
            bg="#2e2e2e"
        )
        self.exit_section_label.pack(pady=10)

        # Botón Salir
        self.exit_button = tk.Button(
            self.exit_section_frame, 
            text="SALIR", 
            command=self.exit_program, 
            font=("Arial", 14, "bold"), 
            bg="#F44336",  # Rojo
            fg="white", 
            width=20
        )
        self.exit_button.pack(pady=10)

        # Listado de procesos ejecutados
        self.processes = []

    def open_main_functions(self):
        # Ejecutar el archivo cliente.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\OneDrive\Documents\MonitorPC\cliente\cliente.py"
        ])
        self.processes.append(process)

    def access1(self):
        # Ejecutar el archivo mostrar_pantalla.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\OneDrive\Documents\MonitorPC\cliente\mostrar_pantalla.py"
        ])
        self.processes.append(process)

    def access2(self):
        # Ejecutar el archivo ver_pantalla.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\OneDrive\Documents\MonitorPC\cliente\ver_pantalla.py"
        ])
        self.processes.append(process)

    def access3(self):
        # Ejecutar el archivo exhibir_client.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\OneDrive\Documents\MonitorPC\cliente\exhibir_client.py"
        ])
        self.processes.append(process)

    def exit_program(self):
        # Detener los procesos ejecutados
        for process in self.processes:
            try:
                process.terminate()  # Detener el proceso
            except psutil.NoSuchProcess:
                pass  # Si el proceso ya terminó, ignoramos el error
        self.processes.clear()  # Limpiar la lista de procesos
        # Mantener solo el menú activo
        print("Procesos detenidos. El menú sigue disponible.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZAMTronixApp(root)
    root.mainloop()