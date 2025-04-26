import React from 'react';

export default function RoomCard({ room, sensors, actuators, onToggle }) {
  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: 8,
      padding: 16,
      margin: 8,
      width: 240
    }}>
      <h2>{room.replace('_', ' ').toUpperCase()}</h2>

      <div>
        <strong>Sensores:</strong>
        <ul>
          <li>Temp: {sensors.temperature ?? '––'}°C</li>
          <li>Lum: {sensors.luminosity ?? '––'}</li>
          <li>Presença: {sensors.presence ?? '––'}</li>
        </ul>
      </div>

      <div>
        <strong>Atuadores:</strong>
        <ul>
          {Object.entries(actuators).map(([act, state]) => (
            <li key={act}>
              {act.toUpperCase()}:&nbsp;
              <button
                onClick={() => onToggle(room, act, !state)}
                style={{ cursor: 'pointer', backgroundColor: state ? '#f44336' : '#4CAF50', color: 'white', border: 'none', borderRadius: 4, padding: '4px 8px' }}
              >
                {state ? 'Desligar' : 'Ligar'}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
