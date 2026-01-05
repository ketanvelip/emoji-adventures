import React from 'react'
import './GameOver.css'

function GameOver({ onRestart }) {
  return (
    <div className="game-over">
      <div className="game-over-content">
        <div className="game-over-icon">🎭</div>
        <h2>Adventure Complete!</h2>
        <p>Your story has come to an end. Ready for another adventure?</p>
        <button className="restart-button" onClick={onRestart}>
          Start New Adventure
        </button>
      </div>
    </div>
  )
}

export default GameOver
