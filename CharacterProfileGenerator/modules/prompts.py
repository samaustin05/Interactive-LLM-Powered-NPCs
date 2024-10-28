# prompts.py

def get_world_description_prompt(scraped_game_text):
    return (
        "Based on the following information about the game, provide a detailed description of the game world, "
        "including its setting, major events, and any important details that a person living in that world should know. "
        "Do not include any information about the development, the release of the videogame itself, or anything outside the context of the game."
        "Please output this in paragraph form without any additional text, comments, or explanations.\n"
        f"{scraped_game_text}"
    )

def get_public_info_prompt(scraped_game_text):
    return (
        "Based on the following information about the game, provide comprehensive public information about the game world, "
        "including major events, key locations, and important details that are essential for understanding the context of the game. "
        "Do not include any information about the development, the release of the videogame itself, or anything outside the context of the game."
        "Please output this in paragraph form without any additional text, comments, or explanations.\n"
        f"{scraped_game_text}"
    )

def get_bio_prompt(scraped_character_text):
    return (
        "Based on the following information about this character, provide a comprehensive and detailed biography for the character. "
        "Include information about their background, personality, relationships, abilities, and role in the game's story. "
        "Do not include any information about the development, the release of the videogame itself, or anything outside the context of the game."
        "Please output this in paragraph form without any additional text, comments, or explanations.\n"
        f"{scraped_character_text}"
    )

def get_knowledge_prompt(scraped_character_text):
    return (
        "Based on the following information about this character, provide detailed secret knowledge that they possess which is not present in the public database. "
        "This should include hidden abilities, undisclosed information about the game world, or any other secret details that enrich the character's depth. "
        "Do not include any information about the development, the release of the videogame itself, or anything outside the context of the game."
        "Please output this in paragraph form without any additional text, comments, or explanations.\n"
        f"{scraped_character_text}"
    )

def get_pre_conversation_prompt(scraped_character_text):
    return (
        f"Based on the following information about this character, write exactly 30 common dialogues "
        f"that the character would say. The output must be a valid JSON object with a key 'pre_conversation' "
        f"that maps to a list of dialogue objects. Each dialogue object should have a single key 'line' "
        f"with the dialogue string as its value. Do not include any additional text, comments, or explanations.\n\n"
        f"Example Output:\n"
        f"```json\n"
        f"{{\n"
        f'  "pre_conversation": [\n'
        f'    {{ "line": "Character: Sample dialogue 1" }},\n'
        f'    {{ "line": "Character: Sample dialogue 2" }},\n'
        f'    {{ "line": "Character: Sample dialogue 3" }}\n'
        f'  ]\n'
        f"}}\n"
        f"```\n\n"
        f"{scraped_character_text}"
    )

def get_conversation_prompt(scraped_character_text):
    return (
        f"Based on the following information about this character, please provide exactly 10 lines of dialogue that "
        f"the character would say in the world. The output must be a valid JSON object with a key 'conversation' "
        f"that maps to a list of objects. Each object should have two keys: 'sender' and 'message'. "
        f"'sender' contains the name of the speaker, and 'message' contains the dialogue text. "
        f"Do not include any additional text, comments, or explanations.\n\n"
        f"Example Output:\n"
        f"```json\n"
        f"{{\n"
        f'  "conversation": [\n'
        f'    {{\n'
        f'      "sender": "Character",\n'
        f'      "message": "line\n'
        f'    }},\n'
        f'    {{\n'
        f'      "sender": "Character",\n'
        f'      "message": "line"\n'
        f'    }}\n'
        f'  ]\n'
        f"}}\n"
        f"```\n\n"
        f"{scraped_character_text}"
    )
