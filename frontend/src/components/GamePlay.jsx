import React, { useState, useEffect } from 'react'
import axios from 'axios'
import StoryDisplay from './StoryDisplay'
import EmojiInput from './EmojiInput'
import TurnCounter from './TurnCounter'
import './GamePlay.css'

function GamePlay({ genre, onGameStart, onGameOver }) {
  const [sessionId, setSessionId] = useState(null)
  const [story, setStory] = useState('')
  const [turn, setTurn] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [gameOverMessage, setGameOverMessage] = useState(null)

  useEffect(() => {
    startGame()
  }, [])

  const startGame = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await axios.post('/api/game/start', { genre })
      
      console.log('Game started, response:', response.data)
      console.log('Story received:', response.data.story)
      
      setSessionId(response.data.session_id)
      setStory(response.data.story)
      setTurn(response.data.turn)
      
      onGameStart(response.data.session_id)
      setLoading(false)
    } catch (err) {
      console.error('Error starting game:', err)
      setError('Failed to start game. Please try again.')
      setLoading(false)
    }
  }

  const handleEmojiSubmit = async (emojis) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await axios.post('/api/game/continue', {
        session_id: sessionId,
        emojis: emojis
      })
      
      setStory(response.data.story)
      setTurn(response.data.turn)
      
      if (response.data.game_over) {
        setGameOverMessage(response.data.game_over_reason || 'Your adventure has concluded.')
      }
      
      setLoading(false)
    } catch (err) {
      console.error('Error continuing game:', err)
      setError(err.response?.data?.detail || 'Failed to continue game. Please try again.')
      setLoading(false)
    }
  }

  if (loading && !story) {
    return <div className="loading">Starting your adventure...</div>
  }

  return (
    <div className="gameplay">
      <div className="gameplay-left">
        {error && (
          <div className="error">{error}</div>
        )}
        
        <StoryDisplay story={story} />
        
        {loading && story && (
          <div className="loading-inline">AI is crafting your story...</div>
        )}
      </div>
      
      <div className="gameplay-right">
        <TurnCounter current={turn} max={30} />
        
        {gameOverMessage ? (
          <div className="game-over-banner">
            <div>{gameOverMessage}</div>
            <button 
              className="restart-button"
              onClick={onGameOver}
            >
              Start New Adventure
            </button>
          </div>
        ) : (
          <EmojiInput 
            onSubmit={handleEmojiSubmit} 
            disabled={loading}
          />
        )}
      </div>
    </div>
  )
}

export default GamePlay
