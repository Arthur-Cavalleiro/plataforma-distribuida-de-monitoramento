#!/usr/bin/env python3
"""
Simulador de Sensores para a Plataforma de Ambientes Inteligentes
Envia leituras periódicas via UDP para o Gateway.
"""

import asyncio
import json
import random
import time
import argparse

# Definição das salas e sensores
ROOMS = ["coordination", "classroom_A", "classroom_B"]
SENSORS = {
    "temperature": lambda: round(random.uniform(18.0, 28.0), 2),
    "luminosity": lambda: random.randint(0, 1000),
    "presence": lambda: random.choice([0, 1]),  # 0: sem presença, 1: presença
}

async def send_sensor_data(host: str, port: int, interval: float):
    loop = asyncio.get_running_loop()
    while True:
        for room in ROOMS:
            for sensor, fn in SENSORS.items():
                data = {
                    "room": room,
                    "sensor": sensor,
                    "value": fn(),
                    "timestamp": int(time.time())
                }
                message = json.dumps(data).encode("utf-8")
                # Envia via UDP para o gateway
                transport, _ = await loop.create_datagram_endpoint(
                    lambda: asyncio.DatagramProtocol(),
                    remote_addr=(host, port)
                )
                transport.sendto(message)
                transport.close()
        await asyncio.sleep(interval)


def parse_args():
    parser = argparse.ArgumentParser(description="Simula sensores de ambientes inteligentes")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="IP do gateway")
    parser.add_argument("--port", type=int, default=9999, help="Porta UDP do gateway")
    parser.add_argument("--interval", type=float, default=5.0, help="Intervalo entre leituras (segundos)")
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Iniciando simulador de sensores enviando para {args.host}:{args.port} a cada {args.interval}s")
    asyncio.run(send_sensor_data(args.host, args.port, args.interval))


if __name__ == "__main__":
    main()
