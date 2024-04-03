import threading
import zmq
from sender import enviarMensaje

class ActuadorAspersor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://*:5566")  # Asegúrate de que este puerto esté libre y sea el correcto

    def run(self):
        print("Actuador aspersor esperando señales de humo...")
        while True:
            datos = self.socket.recv(1024).decode('utf-8')
            # Divide el mensaje en sus partes componentes
            partes_mensaje = datos.split(' - ')
            sensorTipo_y_resultado, timestamp = partes_mensaje[0], partes_mensaje[1]
            sensorTipo, resultado = sensorTipo_y_resultado.split(': ')
            if resultado == "True":
                print(f"Alerta de humo detectada en sensor {sensorTipo}: Activando aspersor...")
        

if __name__ == "__main__":
    actuador = ActuadorAspersor()
    actuador.start()
