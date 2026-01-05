from typing import List, Dict, Any


GENRE_DESCRIPTIONS = {
    "fantasy": "A magical world filled with dragons, wizards, enchanted forests, and ancient prophecies.",
    "sci-fi": "A futuristic universe with advanced technology, space exploration, aliens, and scientific wonders.",
    "mystery": "A world of intrigue, secrets, investigation, clues, and puzzle-solving.",
    "horror": "A dark and terrifying realm filled with supernatural entities, survival challenges, and psychological terror.",
    "adventure": "An exciting world of exploration, treasure hunting, ancient ruins, and daring escapades."
}


def get_system_prompt(genre: str, turn: int, history: List[Dict[str, Any]]) -> str:
    """Generate system prompt for the story engine."""
    
    history_text = ""
    if history:
        history_text = "\n\nStory Memory (Previous Turns):\n"
        for entry in history[-5:]:  # Last 5 turns for context
            emojis = " ".join(entry.get("emojis", []))
            story = entry.get("story", "")
            history_text += f"Turn {entry.get('turn', 0)}: Player used [{emojis}]\n{story}\n\n"
    
    prompt = f"""You are a creative storytelling AI for an emoji-based adventure game.

Genre: {genre.upper()}
Genre Description: {GENRE_DESCRIPTIONS.get(genre, "An engaging narrative world.")}
Current Turn: {turn}/30

Your Role:
You interpret emoji combinations that players submit and weave them into an engaging, branching narrative.

Core Rules:
1. Interpret emoji combinations creatively but logically within the story context
2. Maintain absolute consistency with previous story events and established world rules
3. Emoji order matters - consider sequence and combinations
4. Allow for failure states - dangerous or foolish choices can lead to story endings
5. Adapt narrative pacing based on turn count:
   - Turns 1-10: Setup, exploration, character establishment
   - Turns 11-20: Rising action, challenges, complications
   - Turns 21-30: Climax and resolution
6. Each response should be 1-2 concise paragraphs (3-4 sentences each)
7. Create vivid, immersive descriptions that match the genre tone but keep them brief
8. Reference previous emoji choices when narratively appropriate
9. If emojis lead to an unrecoverable situation (death, impossible scenario), end the story gracefully

Story State Tracking:
- Remember characters introduced
- Track items/abilities gained through emojis
- Maintain location consistency
- Build on established plot threads
{history_text}"""
    
    return prompt


def get_opening_prompt(genre: str) -> str:
    """Generate prompt for creating the opening scenario."""
    
    return f"""Create an engaging opening scenario for a {genre} adventure.

Requirements:
- 1-2 concise paragraphs (3-4 sentences each) introducing the setting and situation
- Create intrigue and hooks for the player to explore
- Establish the tone matching the {genre} genre
- End with a sense of possibility - the adventure is about to begin
- Do NOT ask questions or give choices - simply set the scene
- Be vivid but concise

Generate the opening now:"""


def get_continuation_prompt(emojis: List[str], current_story: str) -> str:
    """Generate prompt for continuing the story based on emoji input."""
    
    emoji_string = " ".join(emojis)
    
    return f"""The player has submitted these emojis: {emoji_string}

Current Story Context:
{current_story}

Based on the emoji combination and the current story, interpret what the player intends and continue the narrative.

Guidelines:
- Consider what each emoji could represent in this context
- Think about the emoji sequence and combination meaning
- Maintain story continuity and logic
- Create interesting consequences (positive or negative) based on the choice
- If this leads to a story-ending situation (death, failure, victory), clearly narrate the conclusion
- Be creative but grounded in the established narrative

Continue the story now:"""


def get_failure_check_prompt(story: str, emojis: List[str]) -> str:
    """Generate prompt to check if the story has reached a failure/end state."""
    
    emoji_string = " ".join(emojis)
    
    return f"""Analyze if this story segment represents a game-ending situation.

Latest Story:
{story}

Player's Emojis: {emoji_string}

Respond with ONLY one of these exact phrases:
- "CONTINUE" - if the story can logically continue
- "VICTORY" - if the player achieved their goal/won
- "DEFEAT" - if the player died or failed irreversibly
- "CONCLUSION" - if the story reached a natural ending

Your analysis:"""
