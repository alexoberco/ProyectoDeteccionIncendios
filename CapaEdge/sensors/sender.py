# sender.py
import zmq
from datetime import datetime


def enviarMensaje(resultado, sensorTipo):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:5555")  

    mensaje = f"{sensorTipo}: {resultado} - {datetime.now()}"
    socket.send_string(mensaje)

    socket.close()
    context.term()
