import socket
import data
import busy
#On/Off
Status = False
#Host de escuta
HOST = socket.gethostbyname(socket.gethostname())
PORT  = 50000
#Adicionar Dispositivos
Devices = []
def maquina_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    while True:
        s.listen()
        conn, ender = s.accept()
        if ender[0] not in Devices:
            conn.close()
        else:
            for i in busy.mesas_ocupadas1:
                del busy.mesas_ocupadas['{}'.format(i)]
            for i in busy.militantes:
                del busy.mesas_ocupadas['{}'.format(i)]
            busy.militantes = []
            busy.mesas_ocupadas1 = []
            busy.mesas_ocupadas = {}
            data.importar_mesas(file='mesas.txt',dict=busy.mesas_ocupadas,lst=busy.mesas_ocupadas1)
            conn.close()
def devices_allert():
    for i in Devices:
        if i == HOST:
            pass
        else:
            while True:
                try:
                    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    c.connect((i, PORT))
                    c.close()
                    break
                except:
                    continue
    return
