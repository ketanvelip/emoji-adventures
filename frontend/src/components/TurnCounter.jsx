import React from 'react'
import './TurnCounter.css'

function TurnCounter({ current, max }) {
  const percentage = (current / max) * 100

  return (
    <div className="turn-counter">
      <div className="turn-info">
        <span className="turn-label">Turn</span>
        <span className="turn-numbers">{current} / {max}</span>
      </div>
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export default TurnCounter
