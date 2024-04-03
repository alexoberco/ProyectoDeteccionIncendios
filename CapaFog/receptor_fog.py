import zmq

def iniciar_receptor_fog():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")

    # Diccionarios para acumular lecturas y contarlas
    lecturas_humedad = []
    lecturas_temperatura = []
    detecciones_humo = []

    conteo_humedad = 0
    conteo_temperatura = 0
    conteo_humo = 0

    print("Receptor Fog iniciado y esperando mensajes...")
    while True:
        try:
            datos = socket.recv_string()
            # Divide el mensaje en sus partes componentes
            partes_mensaje = datos.split(' - ')
            sensorTipo_y_resultado, timestamp = partes_mensaje[0], partes_mensaje[1]
            sensorTipo, resultado_str = sensorTipo_y_resultado.split(': ')
            resultado = 1 if resultado_str == "True" else 0 if resultado_str == "False" else float(resultado_str)
            print(f"{sensorTipo} con {resultado_str} TIEMPO {timestamp}")
            # Clasifica las lecturas por tipo de sensor y las acumula
            if "Humedad" in sensorTipo and resultado_str != "-1":
                lecturas_humedad.append(resultado)
                conteo_humedad += 1
            elif "Temperatura" in sensorTipo and resultado_str != "-1":
                lecturas_temperatura.append(resultado)
                conteo_temperatura += 1
            elif "Humo" in sensorTipo:
                if resultado_str != "-1":  # Solo cuenta las detecciones de humo (True/False), ignora -1
                    detecciones_humo.append(resultado)
                conteo_humo += 1

            # Verifica si se han recibido 100 lecturas (10 por cada uno de los 10 sensores)
            if conteo_humedad == 10:
                promedio_humedad = sum(lecturas_humedad) / len(lecturas_humedad)
                print(f"Promedio de Humedad: {promedio_humedad:.2f}")
                lecturas_humedad.clear()
                conteo_humedad = 0

            if conteo_temperatura == 10:
                promedio_temperatura = sum(lecturas_temperatura) / len(lecturas_temperatura)
                print(f"Promedio de Temperatura: {promedio_temperatura:.2f}")
                lecturas_temperatura.clear()
                conteo_temperatura = 0

            if conteo_humo == 10:  # Considera las lecturas de True/False, no promedio sino conteo de True
                veces_detectado_humo = sum(detecciones_humo)
                print(f"Humo detectado {veces_detectado_humo} veces de 10.")
                detecciones_humo.clear()
                conteo_humo = 0
            
        except zmq.ZMQError as e:
            print(f"Ha ocurrido un error en la recepción de mensajes: {e}")
            break

if __name__ == "__main__":
    iniciar_receptor_fog()
