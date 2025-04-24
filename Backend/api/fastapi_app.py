from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import zmq, threading, json

app = FastAPI()

# === CORS ===
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estados em memória
ROOMS = ["coordination", "classroom_A", "classroom_B"]
sensors_state = {
    room: {"temperature": None, "luminosity": None, "presence": None}
    for room in ROOMS
}
actuators_state = {
    room: {"ac": False, "lamp1": False, "lamp2": False}
    for room in ROOMS
}

# Modelo de comando
class ActuatorCommand(BaseModel):
    room: str
    actuator: str
    command: str  # "ON" ou "OFF"

# Thread para SUB de sensores (ZMQ PUB do gateway)
def sensor_listener(pub_host: str, pub_port: int):
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://{pub_host}:{pub_port}")
    sub.setsockopt_string(zmq.SUBSCRIBE, "")
    while True:
        msg = sub.recv_string()
        data = json.loads(msg)
        room = data["room"]
        sensor = data["sensor"]
        value = data["value"]
        sensors_state[room][sensor] = value

@app.on_event("startup")
def startup_event():
    # Inicia o listener em background
    t = threading.Thread(
        target=sensor_listener,
        args=("127.0.0.1", 5557),
        daemon=True
    )
    t.start()

@app.get("/api/sensors")
def get_sensors():
    return sensors_state

@app.get("/api/actuators")
def get_actuators():
    return actuators_state

@app.post("/api/actuators")
def post_actuator(cmd: ActuatorCommand):
    # Validação
    if cmd.room not in actuators_state \
       or cmd.actuator not in actuators_state[cmd.room] \
       or cmd.command not in ("ON","OFF"):
        raise HTTPException(status_code=400, detail="Comando inválido")
    # Envia via ZMQ PUSH para o gateway (fila de comandos)
    ctx = zmq.Context()
    push = ctx.socket(zmq.PUSH)
    push.connect("tcp://127.0.0.1:5556")
    push.send_string(cmd.json())
    # Atualiza estado local
    actuators_state[cmd.room][cmd.actuator] = (cmd.command == "ON")
    return {"status":"sent", "command":cmd}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True)
