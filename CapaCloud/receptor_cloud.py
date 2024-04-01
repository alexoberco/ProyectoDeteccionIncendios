# receptor_cloud.py
import zmq
import json
from datetime import datetime


context = zmq.Context()
socket = context.socket(zmq.PULL)

def almacenar_datos(data):
    # Define la ruta al archivo JSON donde se almacenarán los datos
    archivo_datos = "datos_almacenados.json"
    try:
        # Intenta abrir el archivo existente para leer los datos actuales
        with open(archivo_datos, "r") as archivo:
            datos_actuales = json.load(archivo)
    except FileNotFoundError:
        # Si el archivo no existe, comienza con una lista vacía
        datos_actuales = []

    # Añade los nuevos datos a la lista de datos actuales
    datos_actuales.append(data)

    # Escribe los datos actualizados de nuevo al archivo JSON
    with open(archivo_datos, "w") as archivo:
        json.dump(datos_actuales, archivo, indent=4)

def iniciar_receptor_cloud():
    
    socket.bind("tcp://*:5560") 

    print("Receptor Cloud iniciado y esperando datos procesados...")
    while True:
        try:
            data = socket.recv_json()
            print(f"Dato procesado recibido: {data}")
            # Almacena el dato recibido en un archivo JSON
            almacenar_datos(data)
        except zmq.ZMQError as e:
            print(f"Error al recibir datos: {e}")
            break

def generar_alerta(data):
    # Ejemplo de criterio de alerta: temperatura > 30
    if data["tipo"] == "Temperatura" and data["valor"] > 30:
        print("Alerta: Temperatura alta detectada.")


# Modifica la sección donde se recibe y procesa el dato para incluir la generación de alertas
    try:
        data = socket.recv_json()
        print(f"Dato procesado recibido: {data}")
        almacenar_datos(data)
        generar_alerta(data)  # Llama a generar_alerta con los datos recibidos
    except zmq.ZMQError as e:
        print(f"Error al recibir datos: {e}")


if __name__ == "__main__":
    iniciar_receptor_cloud()
