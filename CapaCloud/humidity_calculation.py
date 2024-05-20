import json
import time
from collections import defaultdict

import zmq

def calcular_humedad_mensual():
    while True:
        time.sleep(20)  # Calcular cada 20 segundos
        try:
            datos_por_sensor = defaultdict(list)
            with open('cloud_data.json', 'r') as file:
                for line in file:
                    data = json.loads(line.strip())
                    if 'Humedad' in data['sensorTipo']:
                        datos_por_sensor[data['sensorTipo']].append(float(data['resultado']))
            
            for sensor, lecturas in datos_por_sensor.items():
                if lecturas:
                    humedad_mensual = sum(lecturas) / len(lecturas)
                    print(f"Humidad mensual calculada para {sensor}: {humedad_mensual}")
                    if humedad_mensual < 70:
                        alerta = f"Alerta de humedad mensual baja para {sensor}: {humedad_mensual}"
                        print(alerta)
                        enviar_alerta_sc(alerta)

        except Exception as e:
            print(f"Error al calcular la humedad mensual: {e}")

def enviar_alerta_sc(alerta):
    context = zmq.Context()
    sc_socket = context.socket(zmq.REQ)
    sc_socket.connect("tcp://localhost:5572")
    sc_socket.send_string(alerta)
    sc_socket.recv_string()  # Esperar la confirmación del SC

if __name__ == "__main__":
    calcular_humedad_mensual()
