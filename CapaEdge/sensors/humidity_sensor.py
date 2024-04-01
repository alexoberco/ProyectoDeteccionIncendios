# humidity_sensor.py
import threading
import time
import random
import json
from pathlib import Path
from sender import enviarMensaje

class SensorHumedad(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.probaAcierto = config["acierto"]
        self.probaFuera = config["fuera"]
        self.probaError = config["error"]

    def run(self):
        while True:
            resultado = self.generar_lectura()
            enviarMensaje(resultado, "Humedad")
            time.sleep(5)  # Intervalo entre lecturas para humedad

    def generar_lectura(self):
        proba = random.uniform(0.0, 1.0)
        if proba < self.probaAcierto:
            return random.uniform(70.0, 100.0)
        elif proba < self.probaAcierto + self.probaFuera:
            return random.uniform(0.0, 69.9)  # Asumiendo que "fuera de rango" es por debajo del rango normal
        else:
            return -1

if __name__ == "__main__":
    current_directory = Path(__file__).parent
    config_path = current_directory.parent / "config.json"

    with open(config_path, "r") as file:
        config = json.load(file)["humedad"]
    
    sensor = SensorHumedad(config)
    sensor.start()
