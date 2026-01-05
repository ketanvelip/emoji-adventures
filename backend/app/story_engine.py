import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from app.models import Genre
from app.prompts import (
    get_system_prompt,
    get_opening_prompt,
    get_continuation_prompt,
    get_failure_check_prompt
)


class StoryEngine:
    """AI-powered story generation and emoji interpretation engine."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def generate_opening(self, genre: Genre) -> str:
        """Generate the opening scenario for a new game."""
        
        try:
            system_prompt = get_system_prompt(genre.value, 1, [])
            user_prompt = get_opening_prompt(genre.value)
            combined_input = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.client.responses.create(
                model=self.model,
                input=combined_input
            )
            
            # Responses API structure: response.output[0].content
            content = response.output[0].content
            if isinstance(content, list):
                story = content[0].text if hasattr(content[0], 'text') else str(content[0])
            else:
                story = content
            
            story = story.strip() if isinstance(story, str) else str(story)
            
            if story:
                print(f"GPT-5 generated story successfully: {len(story)} characters")
                return story
            
            print("GPT-5 returned empty content, using fallback")
            return self._get_fallback_opening(genre)
        
        except Exception as e:
            print(f"Error generating opening: {e}")
            return self._get_fallback_opening(genre)
    
    def interpret_and_continue(
        self,
        emojis: List[str],
        genre: Genre,
        turn: int,
        history: List[Dict[str, Any]]
    ) -> str:
        """Interpret emoji input and continue the story."""
        
        current_story = history[-1]["story"] if history else ""
        
        try:
            system_prompt = get_system_prompt(genre.value, turn, history)
            user_prompt = get_continuation_prompt(emojis, current_story)
            combined_input = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.client.responses.create(
                model=self.model,
                input=combined_input
            )
            
            # Responses API structure: response.output[0].content
            content = response.output[0].content
            if isinstance(content, list):
                story = content[0].text if hasattr(content[0], 'text') else str(content[0])
            else:
                story = content
            
            story = story.strip() if isinstance(story, str) else str(story)
            
            if story:
                print(f"GPT-5 continued story successfully: {len(story)} characters")
                return story
            
            print("GPT-5 returned empty content, using fallback")
            return self._get_fallback_continuation(emojis)
        
        except Exception as e:
            print(f"Error continuing story: {e}")
            return self._get_fallback_continuation(emojis)
    
    def check_game_state(
        self,
        story: str,
        emojis: List[str]
    ) -> tuple[bool, Optional[str]]:
        """
        Check if the game has reached an ending state.
        
        Returns:
            (game_over: bool, reason: Optional[str])
        """
        
        try:
            system_context = "You are a game state analyzer. Respond with only the exact phrase requested."
            user_prompt = get_failure_check_prompt(story, emojis)
            combined_input = f"{system_context}\n\n{user_prompt}"
            
            response = self.client.responses.create(
                model=self.model,
                input=combined_input
            )
            
            # Responses API structure: response.output[0].content
            content = response.output[0].content
            if isinstance(content, list):
                result = content[0].text if hasattr(content[0], 'text') else str(content[0])
            else:
                result = content
            
            result = result.strip().upper() if isinstance(result, str) else str(result).upper()
            
            if "VICTORY" in result:
                return True, "Victory! You've achieved your goal."
            elif "DEFEAT" in result:
                return True, "Defeat. Your journey ends here."
            elif "CONCLUSION" in result:
                return True, "The story has reached its natural conclusion."
            else:
                return False, None
        
        except Exception as e:
            print(f"Error checking game state: {e}")
            return False, None
    
    def _get_fallback_opening(self, genre: Genre) -> str:
        """Fallback opening if API fails."""
        
        fallbacks = {
            Genre.FANTASY: "You stand at the edge of the Whispering Woods, an ancient map clutched in your hand. The trees seem to lean in, as if listening to your thoughts. A golden light flickers deeper in the forest, beckoning you forward.",
            Genre.SCIFI: "You wake from cryosleep aboard the starship Endeavor. Red warning lights pulse across the bridge. The navigation system shows you've drifted far off course - into uncharted space.",
            Genre.MYSTERY: "Rain hammers the windows of your detective office. A mysterious envelope slides under your door. Inside: a single photograph of a missing person, and coordinates to an abandoned warehouse.",
            Genre.HORROR: "The old mansion looms before you, its windows like hollow eyes. You were hired to spend one night here to claim the inheritance. But as you step inside, the door slams shut behind you.",
            Genre.ADVENTURE: "The treasure map you found in your grandfather's attic leads here - to the mouth of an unexplored cave system. Your flashlight beam reveals ancient markings on the walls. Adventure awaits."
        }
        
        return fallbacks.get(genre, "Your adventure begins in a mysterious place. What will you do?")
    
    def _get_fallback_continuation(self, emojis: List[str]) -> str:
        """Fallback continuation if API fails."""
        
        emoji_str = " ".join(emojis)
        return f"You use {emoji_str} in your next action. The situation evolves in unexpected ways, leading you deeper into the adventure."
