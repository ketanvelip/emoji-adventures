import os
import uuid
import time
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models import (
    StartGameRequest,
    StartGameResponse,
    ContinueGameRequest,
    ContinueGameResponse,
    GameSession
)
from app.story_engine import StoryEngine

load_dotenv()

app = FastAPI(title="Emoji Adventures API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

story_engine = StoryEngine()

sessions: Dict[str, GameSession] = {}

SESSION_TIMEOUT = 1800
MAX_TURNS = 30


def cleanup_old_sessions():
    """Remove sessions older than SESSION_TIMEOUT."""
    current_time = time.time()
    expired = [
        sid for sid, session in sessions.items()
        if current_time - session.last_activity > SESSION_TIMEOUT
    ]
    for sid in expired:
        del sessions[sid]
        print(f"Cleaned up expired session: {sid}")


@app.get("/")
def read_root():
    return {"message": "Emoji Adventures API", "active_sessions": len(sessions)}


@app.post("/api/game/start", response_model=StartGameResponse)
def start_game(request: StartGameRequest):
    """Start a new game session."""
    
    cleanup_old_sessions()
    
    session_id = str(uuid.uuid4())
    
    opening_story = story_engine.generate_opening(request.genre)
    print(f"Generated opening story: {opening_story[:100]}...")  # Log first 100 chars
    
    session = GameSession(
        session_id=session_id,
        genre=request.genre,
        turn=1,
        history=[{
            "turn": 1,
            "emojis": [],
            "story": opening_story
        }],
        story_state={
            "characters": [],
            "items": [],
            "locations": []
        },
        game_over=False,
        last_activity=time.time()
    )
    
    sessions[session_id] = session
    
    return StartGameResponse(
        session_id=session_id,
        story=opening_story,
        turn=1,
        game_over=False
    )


@app.post("/api/game/continue", response_model=ContinueGameResponse)
def continue_game(request: ContinueGameRequest):
    """Continue the game with emoji input."""
    
    cleanup_old_sessions()
    
    session = sessions.get(request.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.game_over:
        raise HTTPException(status_code=400, detail="Game is already over")
    
    if not request.emojis or len(request.emojis) < 2 or len(request.emojis) > 4:
        raise HTTPException(
            status_code=400,
            detail="Please provide 2-4 emojis"
        )
    
    session.turn += 1
    session.last_activity = time.time()
    
    new_story = story_engine.interpret_and_continue(
        emojis=request.emojis,
        genre=session.genre,
        turn=session.turn,
        history=session.history
    )
    
    session.history.append({
        "turn": session.turn,
        "emojis": request.emojis,
        "story": new_story
    })
    
    game_over, game_over_reason = story_engine.check_game_state(
        new_story,
        request.emojis
    )
    
    if session.turn >= MAX_TURNS:
        game_over = True
        game_over_reason = "Your adventure concludes after an epic journey!"
    
    session.game_over = game_over
    
    return ContinueGameResponse(
        story=new_story,
        turn=session.turn,
        game_over=game_over,
        game_over_reason=game_over_reason
    )


@app.delete("/api/game/end/{session_id}")
def end_game(session_id: str):
    """End a game session and clean up."""
    
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session ended successfully"}
    
    return {"message": "Session not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
