import zmq
import json
from datetime import datetime

def almacenar_datos(sensorTipo, lote, resultado, timestamp):
    # Almacenar los datos en un archivo JSON o una base de datos
    data = {
        'sensorTipo': sensorTipo,
        'lote': lote,
        'resultado': resultado,
        'timestamp': timestamp
    }
    with open('cloud_data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

def iniciar_proxy_cloud():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5556")

    # Conectar al SC de la nube
    sc_socket = context.socket(zmq.REQ)
    sc_socket.connect("tcp://localhost:5572")

    print("Proxy Cloud iniciado y esperando mensajes...")
    while True:
        try:
            datos = socket.recv(1024).decode('utf-8')
            partes = datos.split(" - ")
            info, timestamp = partes[0], partes[1]
            sensorTipo, lote_str, resultado_str = info.split(":")
            lote = int(lote_str.strip())
            sensorTipo = sensorTipo.strip()
            resultado = resultado_str.strip()
            
            # Almacenar datos recibidos
            almacenar_datos(sensorTipo, lote, resultado, timestamp)
            
            print(f"Datos recibidos y almacenados: {sensorTipo} Lote {lote} Resultado {resultado} Timestamp {timestamp}")

            # Enviar alerta al SC si es necesario
            if resultado == 'True' or (sensorTipo == "Humedad" and float(resultado) < 70.0):
                alerta = f"Alerta de {sensorTipo} en Lote {lote}: {resultado}"
                sc_socket.send_string(alerta)
                sc_socket.recv_string()  # Esperar la confirmación del SC

        except zmq.ZMQError as e:
            print(f"Ha ocurrido un error en la recepción de mensajes: {e}")
            break

if __name__ == "__main__":
    iniciar_proxy_cloud()
