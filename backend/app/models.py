from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum


class Genre(str, Enum):
    FANTASY = "fantasy"
    SCIFI = "sci-fi"
    MYSTERY = "mystery"
    HORROR = "horror"
    ADVENTURE = "adventure"


class StartGameRequest(BaseModel):
    genre: Genre


class StartGameResponse(BaseModel):
    session_id: str
    story: str
    turn: int
    game_over: bool


class ContinueGameRequest(BaseModel):
    session_id: str
    emojis: List[str]


class ContinueGameResponse(BaseModel):
    story: str
    turn: int
    game_over: bool
    game_over_reason: Optional[str] = None


class GameSession(BaseModel):
    session_id: str
    genre: Genre
    turn: int
    history: List[Dict[str, Any]]
    story_state: Dict[str, Any]
    game_over: bool
    last_activity: float
