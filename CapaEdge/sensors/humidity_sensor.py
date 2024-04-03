# humidity_sensor.py
import threading
import time
import random
import json
from pathlib import Path
from sender import enviarMensaje

class SensorHumedad(threading.Thread):
    def __init__(self, config, nombre):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.probaAcierto = config["acierto"]
        self.probaFuera = config["fuera"]
        self.probaError = config["error"]
        self.lote_actual = 1  # Iniciar el contador de lote en 1

    def run(self):
        while True:
            resultado = self.generar_lectura()
            enviarMensaje(self.lote_actual, resultado, self.nombre)
            self.lote_actual += 1
            if self.lote_actual % 20 == 1:
                self.lote_actual = 1
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
    config_path = current_directory.parent / "configs/config_humidity.json"

    with open(config_path, "r") as file:
        config = json.load(file)["humedad"]
    
    # Crear y ejecutar 10 instancias del sensor de humedad
    for i in range(1, 11):
        sensor = SensorHumedad(config, f"Humedad{i}")
        sensor.start()
