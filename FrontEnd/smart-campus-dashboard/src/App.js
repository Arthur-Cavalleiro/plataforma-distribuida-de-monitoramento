import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RoomCard from './components/RoomCard';

const API = 'http://localhost:8000/api';

function App() {
  const rooms = ['coordination', 'classroom_A', 'classroom_B'];

  const [sensors, setSensors]   = useState({});
  const [actuators, setActuators] = useState({});

  // busca estados na API
  const fetchStates = async () => {
    try {
      const [sRes, aRes] = await Promise.all([
        axios.get(`${API}/sensors`),
        axios.get(`${API}/actuators`)
      ]);
      console.log('sensors', sRes.data);
      console.log('actuators', aRes.data);
      setSensors(sRes.data);
      setActuators(aRes.data);
    } catch (err) {
      console.error('Erro ao carregar estados:', err);
    }
  };

  // toggle de atuador
  const handleToggle = async (room, actuator, newState) => {
    try {
      await axios.post(`${API}/actuators`, {
        room, actuator, command: newState ? 'ON' : 'OFF'
      });
      // já refletimos imediatamente
      setActuators(prev => ({
        ...prev,
        [room]: { ...prev[room], [actuator]: newState }
      }));
    } catch (err) {
      console.error('Erro ao enviar comando:', err);
    }
  };

  useEffect(() => {
    fetchStates();
    const id = setInterval(fetchStates, 2000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>Smart Campus Dashboard</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {rooms.map(room => (
          <RoomCard
            key={room}
            room={room}
            sensors={sensors[room] || {}}
            actuators={actuators[room] || {}}
            onToggle={handleToggle}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
