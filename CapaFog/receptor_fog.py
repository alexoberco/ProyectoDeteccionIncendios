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
            mensaje = socket.recv_string()
            print(f"Mensaje recibido: {mensaje}")
            
        except zmq.ZMQError as e:
            print(f"Ha ocurrido un error en la recepción de mensajes: {e}")
            break

if __name__ == "__main__":
    iniciar_receptor_fog()
