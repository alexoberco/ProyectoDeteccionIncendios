import zmq

def iniciar_sistema_calidad(puerto):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{puerto}")

    print(f"SC iniciado en el puerto {puerto} y esperando alertas...")
    while True:
        try:
            mensaje = socket.recv_string()
            print(f"Alerta recibida: {mensaje}")
            socket.send_string("ACK")
        except zmq.ZMQError as e:
            print(f"Error en SC: {e}")
            break

if __name__ == "__main__":
    puertos = ["5570", "5571", "5572"]  # Puertos para cada capa
    for puerto in puertos:
        iniciar_sistema_calidad(puerto)
