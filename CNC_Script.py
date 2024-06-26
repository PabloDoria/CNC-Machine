import tkinter as tk
from tkinter import messagebox
import serial
import time

class CNCControlApp:
    def init(self, master):
        self.master = master
        self.master.title("CNC Control")

        # Configurar el puerto serial
        try:
            self.serial_port = serial.Serial('COM3', 115200, timeout=1)
            time.sleep(2)  # Espera 2 segundos para que el puerto se inicialice
            self.send_gcode_command('$H')  # Realizar el homing al iniciar
            time.sleep(5)  # Espera 5 segundos para completar el movimiento
            # Volver a la posición inicial
            self.send_gcode_command('G01 X0 Y0 F6000')
            time.sleep(5)  # Espera 5 segundos para completar el movimiento
            self.read_response()

        except serial.SerialException as e:
            messagebox.showerror("Error", f"No se pudo abrir el puerto COM3: {e}")
            self.master.destroy()

        # Definir las posiciones (ajusta las coordenadas según sea necesario)
        self.positions = [
            (0, 0), (19, 0), (38, 0), (57, 0), (76, 0), (93, 0),
            (0, 17.22), (19, 17.22), (38, 17.22), (57, 17.22), (76, 17.22), (93, 17.22),
            (0, 38), (19, 38), (38, 38), (57, 38), (76, 38), (93, 38),
            (0, 52), (19, 52), (38, 52), (57, 52), (76, 52), (93, 52)
        ]

        # Crear botones
        self.create_widgets()

    def create_widgets(self):
        for i, pos in enumerate(self.positions):
            row = i // 6
            col = i % 6
            btn = tk.Button(self.master, text=f"Posición {i+1}", command=lambda p=pos: self.move_to_position(p))
            btn.grid(row=row, column=col, padx=5, pady=5)

        # Botón para detener la máquina
        self.btn_fill = tk.Button(self.master, text="Llenar todos los tubos", command=self.fill_all(self.positions))
        self.btn_fill.grid(row=4, column=0, columnspan=6, pady=10)

        # Botón para detener la máquina
        self.btn_stop = tk.Button(self.master, text="Detener Máquina", command=self.stop_machine)
        self.btn_stop.grid(row=4, column=0, columnspan=6, pady=10)

    def send_gcode_command(self, command):
        try:
            self.serial_port.write((command + '\n').encode())
            print(f"Comando enviado: {command}")
        except Exception as e:
            print(f"Error al enviar el comando: {e}")

    def read_response(self):
        try:
            while self.serial_port.in_waiting > 0:
                response = self.serial_port.readline().decode().strip()
                print(f"Respuesta: {response}")
        except Exception as e:
            print(f"Error al leer la respuesta: {e}")

    def move_to_position(self, position):
        x, y = position
        try:
            # Mover a la posición especificada
            self.send_gcode_command(f'G01 X{x} Y{y} F5000')
            time.sleep(5)  # Espera 5 segundos para completar el movimiento
            self.read_response()

            # Abrir el extrusor
            self.send_gcode_command('M3 S1000')
            time.sleep(2)  # Espera 2 segundos para abrir el extrusor
            self.read_response()

            if x == 0 and y == 0:
                # Tiempo que el extrusor inyecta agua P = tiempo
                self.send_gcode_command('G4 P4.5')
                time.sleep(2)  # Espera 2 segundos para abrir el extrusor
                self.read_response()
            else:
                # Tiempo que el extrusor inyecta agua P = tiempo
                self.send_gcode_command('G4 P6')
                time.sleep(2)  # Espera 2 segundos para abrir el extrusor
                self.read_response()

            # Abrir el extrusor
            self.send_gcode_command('M3 S0')
            time.sleep(2)  # Espera 2 segundos para abrir el extrusor
            self.read_response()

            # Volver a la posición inicial
            self.send_gcode_command('G01 X0 Y0 F5000')
            time.sleep(5)  # Espera 5 segundos para completar el movimiento
            self.read_response()
        except Exception as e:
            print(f"Error al mover a la posición {x}, {y}: {e}")

    def fill_all(self, posiciones):
        for posicion in posiciones:
            x, y = posicion

            try:
                # Mover a la posición especificada
                self.send_gcode_command(f'G01 X{x} Y{y} F5000')
                time.sleep(5)  # Espera 5 segundos para completar el movimiento
                self.read_response()

                # Abrir el extrusor
                self.send_gcode_command('M3 S1000')
                time.sleep(2)  # Espera 2 segundos para abrir el extrusor
                self.read_response()

                if x == 0 and y == 0:
                    # Tiempo que el extrusor inyecta agua P = tiempo
                    self.send_gcode_command('G4 P4.5')
                    time.sleep(2)  # Espera 2 segundos para abrir el extrusor
                    self.read_response()
                else:
                    # Tiempo que el extrusor inyecta agua P = tiempo
                    self.send_gcode_command('G4 P6')
                    time.sleep(2)  # Espera 2 segundos para abrir el extrusor
                    self.read_response()

                # Abrir el extrusor
                self.send_gcode_command('M3 S0')
                time.sleep(2)  # Espera 2 segundos para abrir el extrusor
                self.read_response()

                # Volver a la posición inicial
                self.send_gcode_command('G01 X0 Y0 F5000')
                time.sleep(5)  # Espera 5 segundos para completar el movimiento
                self.read_response()
            except Exception as e:
                print(f"Error al mover a la posición {x}, {y}: {e}")

    def stop_machine(self):
        try:
            # Volver a la posición inicial
            self.send_gcode_command('$H')
            time.sleep(5)  # Espera 5 segundos para completar el movimiento
            self.read_response()

            # Detener la máquina
            self.send_gcode_command('M0')
            self.read_response()
            messagebox.showinfo("CNC Control", "La máquina se ha detenido.")
        except Exception as e:
            print(f"Error al detener la máquina: {e}")

    def on_closing(self):
        if self.serial_port.is_open:
            self.serial_port.close()
        self.master.destroy()


if name == 'main':
    root = tk.Tk()
    app = CNCControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()