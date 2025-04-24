#!/usr/bin/env python3
"""
Gateway Simulado usando ZeroMQ (pyzmq)

- Recebe mensagens UDP de sensores e:
    • envia via ZMQ PUSH para o serviço de controle
    • publica via ZMQ PUB para o FastAPI
- Recebe comandos via ZMQ PULL e encaminha UDP para atuadores.
"""
import socket
import threading
import argparse
import zmq

def udp_to_zmq(push_socket, pub_socket, host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[Gateway] UDP listener ativo em {host}:{port}")
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode('utf-8')
        print(f"[Gateway] Sensor de {addr}: {msg}")
        # para o controle automático
        push_socket.send_string(msg)
        # para o FastAPI / React
        pub_socket.send_string(msg)

def zmq_to_udp(pull_socket, actuator_host: str, actuator_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[Gateway] ZMQ PULL listener ativo (comandos → {actuator_host}:{actuator_port})")
    while True:
        msg = pull_socket.recv_string()
        print(f"[Gateway] Comando p/ atuador: {msg}")
        sock.sendto(msg.encode('utf-8'), (actuator_host, actuator_port))

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--host",        default="127.0.0.1", help="UDP sensores")
    p.add_argument("--port",  type=int, default=9999,      help="porta UDP sensores")
    p.add_argument("--push_port",  type=int, default=5555, help="ZMQ PUSH (serviço de controle)")
    p.add_argument("--pub_port",   type=int, default=5557, help="ZMQ PUB (FastAPI/React)")
    p.add_argument("--pull_port",  type=int, default=5556, help="ZMQ PULL (comandos de atuadores)")
    p.add_argument("--actuator_host", default="127.0.0.1", help="UDP atuadores")
    p.add_argument("--actuator_port", type=int, default=9998, help="porta UDP atuadores")
    return p.parse_args()

def main():
    args = parse_args()
    ctx = zmq.Context()

    # socket PUSH → controle automático
    push_socket = ctx.socket(zmq.PUSH)
    push_socket.bind(f"tcp://*:{args.push_port}")

    # socket PUB → FastAPI
    pub_socket = ctx.socket(zmq.PUB)
    pub_socket.bind(f"tcp://*:{args.pub_port}")

    # socket PULL ← controle automático envia comandos
    pull_socket = ctx.socket(zmq.PULL)
    pull_socket.bind(f"tcp://*:{args.pull_port}")

    # threads de ponte UDP ⇄ ZMQ
    threading.Thread(target=udp_to_zmq,
                     args=(push_socket, pub_socket, args.host, args.port),
                     daemon=True).start()
    threading.Thread(target=zmq_to_udp,
                     args=(pull_socket, args.actuator_host, args.actuator_port),
                     daemon=True).start()

    print(f"[Gateway] Em execução.")
    print(f"  • Sensores UDP {args.host}:{args.port}")
    print(f"  • ZMQ PUSH ↠ controle em tcp://*:{args.push_port}")
    print(f"  • ZMQ PUB ↠ frontend em tcp://*:{args.pub_port}")
    print(f"  • ZMQ PULL ← comandos em tcp://*:{args.pull_port}")
    print(f"  • Atuadores UDP → {args.actuator_host}:{args.actuator_port}")
    try:
        while True: pass
    except KeyboardInterrupt:
        print("[Gateway] Encerrando...")

if __name__ == "__main__":
    main()
