import React from 'react'
import './StoryDisplay.css'

function StoryDisplay({ story }) {
  return (
    <div className="story-display">
      <div className="story-content">
        {story.split('\n').map((paragraph, index) => (
          paragraph.trim() && (
            <p key={index} className="story-paragraph">
              {paragraph}
            </p>
          )
        ))}
      </div>
    </div>
  )
}

export default StoryDisplay
