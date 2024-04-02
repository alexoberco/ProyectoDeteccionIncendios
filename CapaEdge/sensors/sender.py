import zmq
from datetime import datetime

# Utilizando un patrón singleton para el contexto de ZeroMQ
context = zmq.Context()

def enviarMensaje(resultado, sensorTipo, port="5555"):
    try:
        # Reutiliza el mismo contexto para todos los sockets
        socket = context.socket(zmq.PUSH)
        socket.connect(f"tcp://localhost:{port}")
        
        mensaje = f"{sensorTipo}: {resultado} - {datetime.now()}\n"
        socket.send(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    finally:
        socket.close()  # Asegura que el socket siempre se cierre

