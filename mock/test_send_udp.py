import socket
import json

# Endereço do atuador
HOST = "127.0.0.1"
PORT = 9998

# Exemplo de comando: ligar a lamp1 na sala classroom_A
comando = {
    "room": "classroom_A",
    "actuator": "lamp1",
    "command": "ON"
}

# Serializa e envia via UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(comando).encode("utf-8"), (HOST, PORT))
sock.close()

print("Comando enviado:", comando)
