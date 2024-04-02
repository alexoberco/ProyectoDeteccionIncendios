import zmq

def iniciar_receptor_fog():
    context = zmq.Context()
    # Crea un socket de tipo PULL para recibir mensajes
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")  

    print("Receptor Fog iniciado y esperando mensajes...")
    while True:
        # Espera por un mensaje del sensor y lo recibe
        try:
            datos = socket.recv(1024).decode('utf-8')
            # Divide el mensaje en sus partes componentes
            partes_mensaje = datos.split(' - ')
            sensorTipo_y_resultado, timestamp = partes_mensaje[0], partes_mensaje[1]
            sensorTipo, resultado = sensorTipo_y_resultado.split(': ')

            print(f"Mensaje recibido de {sensorTipo} con resultado {resultado} en {timestamp}")
            
            
        except zmq.ZMQError as e:
            print(f"Ha ocurrido un error en la recepción de mensajes: {e}")
            break

if __name__ == "__main__":
    iniciar_receptor_fog()
