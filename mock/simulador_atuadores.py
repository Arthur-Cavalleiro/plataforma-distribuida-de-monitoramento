#!/usr/bin/env python3
"""
Simulador de Atuadores para Plataforma de Ambientes Inteligentes
Escuta comandos UDP enviados pelo gateway e mantém o estado interno dos atuadores.
"""

import socket
import json

# Configuração das salas e atuadores
ROOMS = ["coordination", "classroom_A", "classroom_B"]
ACTUATORS = {
    "ac": False,
    "lamp1": False,
    "lamp2": False,
}

HOST = "127.0.0.1"  # Deve bater com --actuator_host do gateway
PORT = 9998         # Deve bater com --actuator_port do gateway


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Atuador] Escutando comandos em {HOST}:{PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            cmd = json.loads(data.decode("utf-8"))
            room = cmd.get("room")
            actuator = cmd.get("actuator")
            command = cmd.get("command", "").upper()
        except json.JSONDecodeError:
            print(f"[Atuador] Dados inválidos de {addr}: {data}")
            continue

        # Verifica validade
        if room in ROOMS and actuator in ACTUATORS and command in ("ON", "OFF"):
            ACTUATORS[actuator] = (command == "ON")
            estado = "ligado" if ACTUATORS[actuator] else "desligado"
            print(f"[Atuador] Sala {room} – {actuator} agora está {estado}")
        else:
            print(f"[Atuador] Comando inválido recebido: {cmd}")

if __name__ == "__main__":
    main()
