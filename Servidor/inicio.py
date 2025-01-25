import tkinter as tk
import subprocess
import psutil

class ZAMTronixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZAMTronix - Servidor")
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

        # Sección: Monitoreo Remoto
        self.monitoring_remote_frame = tk.Frame(
            root, 
            bd=2, 
            relief="solid", 
            padx=10, pady=10, 
            highlightbackground="#ADD8E6",  # Azul claro
            highlightthickness=2,  # Grosor del contorno
            bg="#2e2e2e"
        )
        self.monitoring_remote_frame.pack(pady=10, padx=10, fill="x")

        self.monitoring_remote_label = tk.Label(
            self.monitoring_remote_frame, 
            text="MONITOREO REMOTO", 
            font=("Arial", 16, "bold"), 
            fg="white", 
            bg="#2e2e2e"
        )
        self.monitoring_remote_label.pack(pady=5)

        # Botón "Observar Pantallas"
        self.observe_screen_button = tk.Button(
            self.monitoring_remote_frame, 
            text="Observar Pantallas", 
            command=self.observe_screen, 
            font=("Arial", 14, "bold"), 
            bg="#2196F3",  # Azul
            fg="white", 
            width=20
        )
        self.observe_screen_button.pack(pady=10)

        # Botón "Mostrar Pantalla"
        self.show_screen_button = tk.Button(
            self.monitoring_remote_frame, 
            text="Mostrar Pantalla", 
            command=self.show_screen, 
            font=("Arial", 14, "bold"), 
            bg="#FF5722",  # Rojo
            fg="white", 
            width=20
        )
        self.show_screen_button.pack(pady=10)

        # Botón "Exhibir Cliente"
        self.exhibit_client_button = tk.Button(
            self.monitoring_remote_frame, 
            text="Exhibir Cliente", 
            command=self.exhibit_client, 
            font=("Arial", 14, "bold"), 
            bg="#9C27B0",  # Morado
            fg="white", 
            width=20
        )
        self.exhibit_client_button.pack(pady=10)

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

        # Lista de procesos ejecutados
        self.processes = []

    def open_main_functions(self):
        # Ejecutar el archivo interfaz_servidor.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\servidor\interfaz_servidor.py"
        ])
        self.processes.append(process)

    def observe_screen(self):
        # Ejecutar el archivo ver_pantalla.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\servidor\ver_pantalla.py"
        ])
        self.processes.append(process)

    def show_screen(self):
        # Ejecutar el archivo mostrar_pantalla.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\servidor\mostrar_pantalla.py"
        ])
        self.processes.append(process)

    def exhibit_client(self):
        # Ejecutar el archivo Exhibir_server.py
        process = subprocess.Popen([
            "python", 
            r"C:\Users\hecto\Documents\TESJI\SEPTIMO SEMESTRE\MonitoreoPC\servidor\Exhibir_server.py"
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
