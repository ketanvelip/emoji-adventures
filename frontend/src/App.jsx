import React, { useState } from 'react'
import GenreSelector from './components/GenreSelector'
import GamePlay from './components/GamePlay'
import GameOver from './components/GameOver'

function App() {
  const [gameState, setGameState] = useState('genre-select')
  const [sessionId, setSessionId] = useState(null)
  const [genre, setGenre] = useState(null)

  const handleGenreSelect = (selectedGenre) => {
    setGenre(selectedGenre)
    setGameState('playing')
  }

  const handleGameStart = (id) => {
    setSessionId(id)
  }

  const handleGameOver = () => {
    setGameState('game-over')
  }

  const handleRestart = () => {
    setGameState('genre-select')
    setSessionId(null)
    setGenre(null)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🎮 Emoji Adventures</h1>
        <p>Create your story with emojis</p>
      </div>
      
      <div className="content">
        {gameState === 'genre-select' && (
          <GenreSelector onSelect={handleGenreSelect} />
        )}
        
        {gameState === 'playing' && (
          <GamePlay
            genre={genre}
            onGameStart={handleGameStart}
            onGameOver={handleGameOver}
          />
        )}
        
        {gameState === 'game-over' && (
          <GameOver onRestart={handleRestart} />
        )}
      </div>
    </div>
  )
}

export default App
