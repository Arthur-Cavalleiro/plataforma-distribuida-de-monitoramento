import socket

HOST = "0.0.0.0"   # escuta em todas as interfaces
PORT = 9999        # mesma porta usada pelo simulador

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"Escutando pacotes UDP em {HOST}:{PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    print("Recebido de", addr, ":", data.decode("utf-8"))
