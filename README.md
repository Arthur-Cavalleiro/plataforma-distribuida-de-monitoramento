# Smart Campus System

## Overview
Este projeto implementa um sistema inteligente de monitoramento e controle de campus que conecta sensores e atuadores de IoT em diversas salas. O sistema utiliza uma arquitetura de microsserviços com processamento de dados em tempo real para automatizar o controle de temperatura e permitir intervenção manual por meio de um painel web.

## System Architecture

```
+----------------+    +----------------+    +----------------+
| Sensor Network |    | Control Service|    | React Frontend |
| (UDP)          |--->| (ZeroMQ)       |<---| (HTTP)         |
+----------------+    +----------------+    +----------------+
        |                     ^                     ^
        v                     |                     |
+--------------------------------------+     +----------------+
| Gateway Service                      |<--->| FastAPI Backend|
| (UDP <-> ZeroMQ bridge)              |     | (REST API)     |
+--------------------------------------+     +----------------+
        |
        v
+----------------+
| Actuator Network|
| (UDP)          |
+----------------+
```

## Components

### Backend
- **FastAPI Application** (Backend/api/fastapi_app.py): REST API that provides sensor data to the frontend and processes actuator commands

### Frontend
- **React Dashboard** (FrontEnd/smart-campus-dashboard): Web interface displaying room data and actuator controls

### Gateway
- **ZeroMQ Bridge** (gateway/gateway.py): Connects UDP-based sensors and actuators with ZeroMQ-based services

### Microservices
- **Control Service** (micro/control_service.py): Implements automatic temperature control logic

### Mocks & Simulators
- **Sensor Simulator** (mock/simulador_sensores.py): Generates mock sensor data
- **Actuator Simulator** (mock/simulador_atuadores.py): Simulates actuator responses
- **UDP Utilities** (mock/udp_listener.py, mock/test_send_udp.py): Test tools for UDP communication

## Setup & Installation

### Backend Requirements
```bash
pip install fastapi uvicorn pyzmq
```

### Frontend Setup
```bash
cd FrontEnd/smart-campus-dashboard
npm install
```

### Gateway & Microservices
```bash
pip install pyzmq
```

## Running the System

1. **Start the Gateway**:
   ```bash
   python gateway/gateway.py
   ```

2. **Start the Control Service**:
   ```bash
   python micro/control_service.py
   ```

3. **Start the Backend API**:
   ```bash
   python Backend/api/fastapi_app.py
   ```

4. **Start the Frontend**:
   ```bash
   cd FrontEnd/smart-campus-dashboard
   npm start
   ```

5. **Start the Simulators** (optional for testing):
   ```bash
   python mock/simulador_sensores.py
   python mock/simulador_atuadores.py
   ```

## Technologies Used

- **Frontend**: React, Axios
- **Backend**: FastAPI, ZeroMQ
- **Communication**: UDP, ZeroMQ (PUB/SUB, PUSH/PULL patterns)
- **Testing**: Mock simulators for sensors and actuators

## Contributors

- Arthur Cavalleiro
- Leonardo Peixoto
- Luan Augusto