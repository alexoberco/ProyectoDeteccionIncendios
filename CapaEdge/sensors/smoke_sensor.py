import threading
import time
import random
import json
import zmq
from pathlib import Path
from sender import enviarMensaje

class SensorHumo(threading.Thread):
    def __init__(self, config, nombre):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.probaAcierto = config["acierto"]
        self.probaError = config["error"]
        self.actuador_aspersor_port = "5566"
        self.lote_actual = 1  # Iniciar el contador de lote en 1

    def run(self):
        while True:
            resultado = self.generar_lectura()
            # Incluir el identificador de lote en el mensaje
            enviarMensaje(self.lote_actual, resultado, self.nombre)
            if resultado:
                enviarMensaje(self.lote_actual, resultado, self.nombre, self.actuador_aspersor_port)
                self.enviar_alerta_sc(f"Humo detectado por {self.nombre}, Lote: {self.lote_actual}, Resultado: {resultado}")
            
            self.lote_actual += 1
            if self.lote_actual % 20 == 1:
                self.lote_actual = 1

            time.sleep(3)  # Intervalo entre lecturas para humo

    def generar_lectura(self):
        proba = random.uniform(0.0, 1.0)
        if proba < self.probaAcierto:
            # Devolver True o False basado en una probabilidad
            return bool(random.getrandbits(1))
        else:
            # Devolver -1 para indicar una lectura inválida o errónea
            return -1
        
    def enviar_alerta_sc(self, mensaje):
        context = zmq.Context()
        sc_socket = context.socket(zmq.REQ)
        sc_socket.connect("tcp://localhost:5566")
        sc_socket.send_string(mensaje)
        sc_socket.recv_string()
        

if __name__ == "__main__":
    current_directory = Path(__file__).parent
    config_path = current_directory.parent / "configs/config_smoke.json"

    with open(config_path, "r") as file:
        config = json.load(file)["humo"]
    
    # Crear y ejecutar 10 instancias del sensor de humo
    for i in range(1, 11):
        sensor = SensorHumo(config, f"Humo{i}")
        sensor.start()
