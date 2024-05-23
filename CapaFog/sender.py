import zmq
from datetime import datetime

# Utilizando un patrón singleton para el contexto de ZeroMQ
context = zmq.Context()

def enviarMensaje(lote, resultado, sensorTipo, port="5556"):
    try:
        socket = context.socket(zmq.PUSH)
        socket.connect(f"tcp://localhost:{port}")
        
        # Incluye el identificador de lote en el mensaje
        mensaje = f"{sensorTipo}:{lote}:{resultado} - {datetime.now()}\n"
        socket.send(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    finally:
        socket.close()
        
def enviarCorreo(lote, resultado, sensorTipo, port="5556"):
    try:
        socket = context.socket(zmq.PUSH)
        socket.connect(f"tcp://localhost:{port}")
        
        # Incluye el identificador de lote en el mensaje
        mensaje = f"Correo: {sensorTipo}:{lote}:{resultado} - {datetime.now()}\n"
        socket.send(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    finally:
        socket.close()
        