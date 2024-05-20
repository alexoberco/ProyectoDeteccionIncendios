import zmq
import time
import subprocess
import platform
import psutil

def start_backup_proxy():
    if platform.system() == "Linux" or platform.system() == "Darwin":  # Darwin para macOS
        subprocess.Popen(['xterm', '-e', 'python3 CapaFog/receptor_fog_backup.py'])
    elif platform.system() == "Windows":
        subprocess.Popen(['start', 'cmd', '/k', 'python CapaFog/receptor_fog_backup.py'], shell=True)

def kill_process_using_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        with proc.oneshot():
            try:
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == port:
                        print(f"Killing process {proc.info['name']} with PID {proc.info['pid']} using port {port}")
                        proc.terminate()
                        proc.wait()
                        return
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

def check_health(primary_ip="localhost", primary_port="5555", health_port="5559"):
    context = zmq.Context()
    primary_socket = context.socket(zmq.REQ)
    primary_socket.connect(f"tcp://{primary_ip}:{health_port}")  # socket para el puerto de receptor
    primary_socket.RCVTIMEO = 1000  # 1 second timeout

    backup_active = False
    backup_socket = context.socket(zmq.REQ)
    backup_socket.connect(f"tcp://{primary_ip}:{health_port}")  # Port para el health check del backup
    backup_socket.RCVTIMEO = 1000  # 1 sec de timeout

    while True:
        try:
            primary_socket.send(b"HEALTH_CHECK")
            message = primary_socket.recv()
            print(f"Primary proxy health check response: {message}")
        except zmq.Again:
            print("Primary proxy did not respond, assuming failure.")
            if not backup_active:
                print("Activating backup proxy...")
                # mata qualquier proceso que este usando el puerto de comunicacion
                kill_process_using_port(primary_port)
                #corre el backup
                start_backup_proxy()
                backup_active = True
        except zmq.ZMQError as e:
            print(f"Primary proxy failed: {e}")
            if not backup_active:
                print("Activating backup proxy...")
                # mata qualquier proceso que este usando el puerto de comunicacion
                kill_process_using_port(primary_port)
                #corre el backup
                start_backup_proxy()
                backup_active = True

        if backup_active:
            try:
                backup_socket.send(b"HEALTH_CHECK")
                message = backup_socket.recv()
                print(f"Backup proxy health check response: {message}")
            except zmq.Again:
                print("Backup proxy did not respond.")
            except zmq.ZMQError as e:
                print(f"Backup proxy failed: {e}")
                break

        time.sleep(5)  # revisa cada 5 secs

if __name__ == "__main__":
    check_health()
