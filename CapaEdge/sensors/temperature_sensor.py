import threading
import time
import random
import json
from pathlib import Path
from sender import enviarMensaje

class SensorTemperatura(threading.Thread):
    def __init__(self, config, nombre):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.probaAcierto = config["acierto"]
        self.probaFuera = config["fuera"]
        self.probaError = config["error"]

    def run(self):
        while True:
            resultado = self.generar_lectura()
            enviarMensaje(resultado, self.nombre)
            time.sleep(6)  # Espera 6 segundos entre lecturas

    def generar_lectura(self):
        proba = random.uniform(0.0, 1.0)
        if proba < self.probaAcierto:
            return random.uniform(11.0, 29.4)
        elif proba < self.probaAcierto + self.probaFuera:
            return random.uniform(10.0, 40.0)
        else:
            return -1

if __name__ == "__main__":
    # Carga la configuración desde config.json
    current_directory = Path(__file__).parent
    config_path = current_directory.parent / "config.json"

    with open(config_path, "r") as file:
        config = json.load(file)["temperatura"]
    
    # Crear y ejecutar 10 instancias del sensor de humedad
    for i in range(1, 11):
        sensor = SensorTemperatura(config, f"Temperatura{i}")
        sensor.start()
