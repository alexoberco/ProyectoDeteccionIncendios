# smoke_sensor.py
import threading
import time
import random
import json
from pathlib import Path
from sender import enviarMensaje

class SensorHumo(threading.Thread):
    def __init__(self, config, nombre):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.probaAcierto = config["acierto"]
        self.probaError = config["error"]
        self.actuador_aspersor_port = "5566"  

    def run(self):
        while True:
            resultado = self.generar_lectura()
            enviarMensaje(resultado, self.nombre)
            if resultado:
                enviarMensaje(resultado, self.nombre, self.actuador_aspersor_port)
            time.sleep(3)  # Intervalo entre lecturas para humo

    def generar_lectura(self):
        proba = random.uniform(0.0, 1.0)
        if proba < self.probaAcierto:
            return bool(random.getrandbits(1))
        else:
            return -1

if __name__ == "__main__":
    current_directory = Path(__file__).parent
    config_path = current_directory.parent / "config.json"

    with open(config_path, "r") as file:
        config = json.load(file)["humo"]
    
    # Crear y ejecutar 10 instancias del sensor de humo
    for i in range(1, 11):
        sensor = SensorHumo(config, f"Humo{i}")
        sensor.start()


