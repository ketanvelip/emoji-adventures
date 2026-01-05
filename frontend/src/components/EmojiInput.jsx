import React, { useState } from 'react'
import EmojiPicker from 'emoji-picker-react'
import './EmojiInput.css'

function EmojiInput({ onSubmit, disabled }) {
  const [selectedEmojis, setSelectedEmojis] = useState([])

  const handleEmojiClick = (emojiData) => {
    if (selectedEmojis.length < 4) {
      setSelectedEmojis([...selectedEmojis, emojiData.emoji])
    }
  }

  const removeEmoji = (index) => {
    setSelectedEmojis(selectedEmojis.filter((_, i) => i !== index))
  }

  const handleSubmit = () => {
    if (selectedEmojis.length >= 2 && selectedEmojis.length <= 4) {
      onSubmit(selectedEmojis)
      setSelectedEmojis([])
    }
  }

  const canSubmit = selectedEmojis.length >= 2 && selectedEmojis.length <= 4 && !disabled

  return (
    <div className="emoji-input">
      <div className="picker-container">
        <EmojiPicker
          onEmojiClick={handleEmojiClick}
          width="100%"
          height="350px"
          searchDisabled={false}
          skinTonesDisabled={true}
          previewConfig={{ showPreview: false }}
        />
      </div>

      <div className="emoji-selection">
        <div className="selected-emojis">
          {selectedEmojis.map((emoji, index) => (
            <div key={index} className="selected-emoji" onClick={() => removeEmoji(index)}>
              <span className="emoji">{emoji}</span>
              <span className="remove-icon">×</span>
            </div>
          ))}
          {selectedEmojis.length === 0 && (
            <div className="placeholder">Select 2-4 emojis to continue your story</div>
          )}
        </div>
      </div>

      <div className="submit-section">
        <div className="emoji-count">
          {selectedEmojis.length} / 4 emojis selected
        </div>
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={!canSubmit}
        >
          Continue Story →
        </button>
      </div>
    </div>
  )
}

export default EmojiInput
