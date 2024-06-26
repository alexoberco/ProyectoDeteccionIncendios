import zmq
import threading

def iniciar_receptor_fog():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")

    health_socket = context.socket(zmq.REP)
    health_socket.bind("tcp://*:5559")  # Port for health check requests

    datos_humedad = []
    datos_temperatura = []
    datos_humo = []

    lote_temp = 1
    lote_humo = 1
    lote_hume = 1
    cont_temp = 0
    cont_humo = 0
    cont_hume = 0

    def handle_health_check():
        while True:
            try:
                message = health_socket.recv()
                if message == b"HEALTH_CHECK":
                    health_socket.send(b"HEALTHY")
            except zmq.ZMQError as e:
                print(f"Health check error: {e}")
                break

    health_thread = threading.Thread(target=handle_health_check)
    health_thread.start()

    print("Receptor Fog iniciado y esperando mensajes...")
    while True:
        try:
            datos = socket.recv(1024).decode('utf-8')
            partes = datos.split(" - ")
            info, timestamp = partes[0], partes[1]
            sensorTipo, lote_str, resultado_str = info.split(":")
            lote = int(lote_str.strip())
            sensorTipo = sensorTipo.strip()
            resultado = resultado_str.strip()

            if "Humo" in sensorTipo:
                if lote_humo == lote:
                    datos_humo.append({'sensor': sensorTipo, 'lote': lote, 'resultado': resultado})
                    cont_humo += 1
                    if cont_humo > 9:
                        resultados = 0
                        for dato in datos_humo:
                            if dato['resultado'] == 'True':
                                resultados += 1
                        print(f"HUMO detectado en el lote {lote} en {resultados} sensores de 10\n")
                else:
                    datos_humo = []
                    cont_humo = 0
                    if lote_humo == 20:
                        lote_humo = 1
                    else:
                        lote_humo = lote
                    datos_humo.append({'sensor': sensorTipo, 'lote': lote, 'resultado': resultado})
                    cont_humo += 1
            elif "Humedad" in sensorTipo:
                if lote_hume == lote:
                    datos_humedad.append({'sensor': sensorTipo, 'lote': lote, 'resultado': resultado})
                    cont_hume += 1
                    if cont_hume > 9:
                        x = 1
                        resultados = 0
                        for dato in datos_humedad:
                            if dato['resultado'] != "-1":
                                resultados += float(dato['resultado'])
                                x += 1
                        promedio_hume = resultados / x
                        print(f"HUMEDAD promedio del lote {lote} es: {promedio_hume}\n")
                else:
                    datos_humedad = []
                    cont_hume = 0
                    if lote_hume == 20:
                        lote_hume = 1
                    else:
                        lote_hume = lote
                    datos_humedad.append({'sensor': sensorTipo, 'lote': lote, 'resultado': resultado})
                    cont_hume += 1
            elif "Temperatura" in sensorTipo:
                if lote_temp == lote:
                    datos_temperatura.append({'sensor': sensorTipo, 'lote': lote, 'resultado': resultado})
                    cont_temp += 1
                    if cont_temp > 9:
                        x = 1
                        resultados = 0
                        for dato in datos_temperatura:
                            if dato['resultado'] != "-1":
                                resultados += float(dato['resultado'])
                                x += 1
                        promedio_temp = resultados / x
                        print(f"TEMPERATURA promedio del lote {lote} es: {promedio_temp}\n")
                else:
                    datos_temperatura = []
                    cont_temp = 0
                    if lote_temp == 20:
                        lote_temp = 1
                    else:
                        lote_temp = lote
                    datos_temperatura.append({'sensor': sensorTipo, 'lote': lote, 'resultado': resultado})
                    cont_temp += 1

        except zmq.ZMQError as e:
            print(f"Ha ocurrido un error en la recepción de mensajes: {e}")
            break

if __name__ == "__main__":
    iniciar_receptor_fog()
