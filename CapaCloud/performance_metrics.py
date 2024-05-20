import zmq
import time
from datetime import datetime

def medir_rendimiento():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5557")
    
    total_mensajes = 0
    tiempos_comunicacion = []

    while True:
        datos = socket.recv_string()
        total_mensajes += 1
        timestamp = datetime.now().timestamp()
        tiempos_comunicacion.append(timestamp)

        if total_mensajes % 100 == 0:
            promedio_tiempo = sum(tiempos_comunicacion) / len(tiempos_comunicacion)
            desviacion_estandar = (sum([(x - promedio_tiempo) ** 2 for x in tiempos_comunicacion]) / len(tiempos_comunicacion)) ** 0.5
            print(f"Total de mensajes: {total_mensajes}")
            print(f"Promedio de tiempo de comunicación: {promedio_tiempo}")
            print(f"Desviación estándar del tiempo de comunicación: {desviacion_estandar}")

if __name__ == "__main__":
    medir_rendimiento()
