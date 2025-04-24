#!/usr/bin/env python3
"""
Microserviço de Controle Automático

- Recebe dados de sensores via ZeroMQ PULL.
- Aplica lógica de controle para ar-condicionado (threshold).
- Envia comandos de atuadores via ZeroMQ PUSH.
"""
import json
import argparse
import zmq


def parse_args():
    parser = argparse.ArgumentParser(description="Microserviço de Controle Automático")
    parser.add_argument("--pull_host", type=str, default="127.0.0.1",
                        help="Endereço do ZeroMQ PUSH (sensors)")
    parser.add_argument("--pull_port", type=int, default=5555,
                        help="Porta do ZeroMQ PUSH para PULL de sensores")
    parser.add_argument("--push_host", type=str, default="127.0.0.1",
                        help="Endereço do ZeroMQ PULL (actuator commands)")
    parser.add_argument("--push_port", type=int, default=5556,
                        help="Porta do ZeroMQ PULL para PUSH de comandos")
    parser.add_argument("--temp_threshold", type=float, default=25.0,
                        help="Threshold de temperatura (°C) para ligar o ar-condicionado")
    return parser.parse_args()


def main():
    args = parse_args()
    context = zmq.Context()

    # Socket PULL: conectar no PUSH do gateway de sensores
    pull = context.socket(zmq.PULL)
    pull.connect(f"tcp://{args.pull_host}:{args.pull_port}")
    print(f"[Control] Conectado em tcp://{args.pull_host}:{args.pull_port} para receber sensores")

    # Socket PUSH: conectar no PULL do gateway de comandos
    push = context.socket(zmq.PUSH)
    push.connect(f"tcp://{args.push_host}:{args.push_port}")
    print(f"[Control] Conectado em tcp://{args.push_host}:{args.push_port} para enviar comandos")

    threshold = args.temp_threshold
    print(f"[Control] Threshold de temperatura para ar-condicionado: {threshold}°C")

    while True:
        msg = pull.recv_string()
        data = json.loads(msg)
        sensor = data.get("sensor")
        room = data.get("room")
        value = data.get("value")

        # Lógica de controle para temperatura
        if sensor == "temperature":
            command = None
            if value >= threshold:
                command = "ON"
            else:
                command = "OFF"

            cmd_msg = json.dumps({
                "room": room,
                "actuator": "ac",
                "command": command
            })
            push.send_string(cmd_msg)
            print(f"[Control] Sala {room}: temp={value}°C -> ar-condicionado {command}")

if __name__ == "__main__":
    main()
