import React from 'react'
import './GenreSelector.css'

const genres = [
  { id: 'fantasy', name: 'Fantasy', icon: '🏰', description: 'Magic, dragons, and ancient prophecies' },
  { id: 'sci-fi', name: 'Sci-Fi', icon: '🚀', description: 'Space exploration and futuristic technology' },
  { id: 'mystery', name: 'Mystery', icon: '🔍', description: 'Investigation, clues, and puzzle-solving' },
  { id: 'horror', name: 'Horror', icon: '👻', description: 'Supernatural terror and survival' },
  { id: 'adventure', name: 'Adventure', icon: '🗺️', description: 'Exploration and treasure hunting' },
]

function GenreSelector({ onSelect }) {
  return (
    <div className="genre-selector">
      <h2>Choose Your Adventure Genre</h2>
      <div className="genre-grid">
        {genres.map((genre) => (
          <button
            key={genre.id}
            className="genre-card"
            onClick={() => onSelect(genre.id)}
          >
            <div className="genre-icon">{genre.icon}</div>
            <div className="genre-name">{genre.name}</div>
            <div className="genre-description">{genre.description}</div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default GenreSelector
