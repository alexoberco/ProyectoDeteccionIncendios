# smoke_sensor.py
import threading
import time
import random
import json
from pathlib import Path
from sender import enviarMensaje

class SensorHumo(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.probaAcierto = config["acierto"]
        self.probaError = config["error"]

    def run(self):
        while True:
            resultado = self.generar_lectura()
            enviarMensaje(resultado, "Humo")
            time.sleep(10)  # Intervalo entre lecturas para humo

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
    
    sensor = SensorHumo(config)
    sensor.start()
