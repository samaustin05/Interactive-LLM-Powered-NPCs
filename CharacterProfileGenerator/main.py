# main.py

import json
import logging
from pathlib import Path
from modules.config import Config
from modules.logger import setup_logging
from modules.cohere_client import CohereClient
from modules.scraper import Scraper
from modules.file_ops import FileOperations
from modules.image_handler import ImageHandler
from modules.voice_setup import VoiceSetup
from modules.notebook_runner import NotebookRunner
from modules.prompts import (
    get_world_description_prompt,
    get_public_info_prompt,
    get_bio_prompt,
    get_knowledge_prompt,
    get_pre_conversation_prompt,
    get_conversation_prompt
)
from modules.generation import generate_json, generate_text
from modules.utils import ensure_complete_text

def main():
    try:
        # Setup Logging
        setup_logging(log_file='logs/create_character.log')
        logging.info("Script started.")
        print("Starting character profile generation...")

        # Load API Keys
        api_keys_data = Config('apikeys.json').data  # Load the JSON data
        api_keys = api_keys_data.get('api_keys', [])  # Get the list of API keys

        # Check for missing keys
        if not api_keys:
            logging.error("API keys not found in apikeys.json")
            raise ValueError("API keys not found in apikeys.json")

        # Extract the Cohere API key from the list
        cohere_api_key = api_keys[0]  # Use the first key

        # Optionally extract SerpAPI API key from the list (if applicable)
        serpapi_api_key = api_keys_data.get('serpapi_api_key')
        if not cohere_api_key:
            logging.error("Cohere API key not found in apikeys.json")
            raise ValueError("Cohere API key not found in apikeys.json")

        # Initialize Cohere Client
        co = CohereClient(cohere_api_key)
        logging.info("Cohere client initialized successfully.")

        # Initialize Modules
        scraper = Scraper()
        file_ops = FileOperations()
        image_handler = ImageHandler(serpapi_api_key)
        voice_setup = VoiceSetup()
        notebook_runner = NotebookRunner()

        config = Config('config.json').data

        # Define Game Paths
        game_name = config['game_name']
        game_url = config['game_url']
        base_game_path = Path(game_name.replace(' ', '_'))
        base_game_path.mkdir(parents=True, exist_ok=True)

        # Scrape Game Page
        logging.info(f"Scraping game page: {game_url}")
        print(f"Scraping game page: {game_url}")
        scraped_game_text = scraper.scrape_fandom_page(game_url)
        logging.debug(f"Length of scraped_game_text: {len(scraped_game_text)} characters.")

        # Generate world.txt
        logging.info("Generating world.txt")
        print("Generating world.txt")
        world_prompt = get_world_description_prompt(scraped_game_text)
        world_description = generate_text(co, world_prompt)
        world_description = ensure_complete_text(
            co,
            world_description,
            "Please continue the description of the game world."
        )
        logging.debug(f"world.txt content length: {len(world_description)} characters.")

        # Generate public_info.txt
        logging.info("Generating public_info.txt")
        print("Generating public_info.txt")
        public_info_prompt = get_public_info_prompt(scraped_game_text)
        public_info = generate_text(co, public_info_prompt)
        public_info = ensure_complete_text(
            co,
            public_info,
            "Please continue providing public information about the game world."
        )
        logging.debug(f"public_info.txt content length: {len(public_info)} characters.")

        # Write world.txt and public_info.txt
        logging.info("Writing world.txt and public_info.txt")
        print("Writing world.txt and public_info.txt")
        file_ops.write_text_file(base_game_path / 'world.txt', world_description)
        file_ops.write_text_file(base_game_path / 'public_info.txt', public_info)

        # Iterate Over Characters
        for character in config['characters']:
            character_name = character['name']
            character_url = character['url']
            image_sources = character['images']

            logging.info(f"Processing character: {character_name}")
            print(f"Processing character: {character_name}")

            # Scrape Character Page
            logging.info(f"Scraping character page: {character_url}")
            print(f"Scraping character page: {character_url}")
            scraped_character_text = scraper.scrape_fandom_page(character_url)
            logging.debug(f"Length of scraped_character_text: {len(scraped_character_text)} characters.")

            # Generate bio.txt
            logging.info(f"Generating bio.txt for {character_name}")
            print(f"Generating bio.txt for {character_name}")
            bio_prompt = get_bio_prompt(scraped_character_text)
            bio = generate_text(co, bio_prompt)
            bio = ensure_complete_text(
                co,
                bio,
                "Please continue the biography of the character."
            )
            logging.debug(f"bio.txt content length: {len(bio)} characters.")

            # Generate character_knowledge.txt
            logging.info(f"Generating character_knowledge.txt for {character_name}")
            print(f"Generating character_knowledge.txt for {character_name}")
            knowledge_prompt = get_knowledge_prompt(scraped_character_text)
            knowledge = generate_text(co, knowledge_prompt)
            knowledge = ensure_complete_text(
                co,
                knowledge,
                "Please continue providing secret knowledge for the character."
            )
            logging.debug(f"character_knowledge.txt content length: {len(knowledge)} characters.")

            # Generate pre_conversation.json
            logging.info(f"Generating pre_conversation.json for {character_name}")
            print(f"Generating pre_conversation.json for {character_name}")
            pre_conversation_prompt = get_pre_conversation_prompt(scraped_character_text)
            pre_conversation = generate_json(
                co,
                pre_conversation_prompt,
                schema = {
                    "type": "object",
                    "properties": {
                        "pre_conversation": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "line": {"type": "string"}
                                },
                                "required": ["line"]
                            }
                        }
                    },
                    "required": ["pre_conversation"]
                },
                retries=3,
                delay=2,
                max_tokens=2000,
                temperature=0.7,
                stop_sequences=["```"]
            )

            # Generate conversation.json
            logging.info(f"Generating conversation.json for {character_name}")
            print(f"Generating conversation.json for {character_name}")
            conversation_prompt = get_conversation_prompt(scraped_character_text)
            conversation = generate_json(
                co,
                conversation_prompt,
                schema = {
                    "type": "object",
                    "properties": {
                        "conversation": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "sender": {"type": "string"},
                                    "message": {"type": "string"}
                                },
                                "required": ["sender", "message"]
                            }
                        }
                    },
                    "required": ["conversation"]
                },

                retries=3,
                delay=2,
                max_tokens=2000,
                temperature=0.7,
                stop_sequences=["```"]
            )

            # Create character files
            logging.info(f"Creating character files for {character_name}")
            print(f"Creating character files for {character_name}")
            character_path = base_game_path / 'characters' / character_name
            character_path.mkdir(parents=True, exist_ok=True)
            file_ops.write_text_file(character_path / 'bio.txt', bio)
            file_ops.write_text_file(character_path / 'character_knowledge.txt', knowledge)
            file_ops.write_json_file(character_path / 'pre_conversation.json', pre_conversation)
            file_ops.write_json_file(character_path / 'conversation.json', conversation)

            # Add Character Images if ImageHandler is initialized
            if image_handler:
                image_handler.add_character_images(character_path, image_sources)
            else:
                logging.info(f"Skipping image addition for {character_name} due to missing SerpAPI key.")

            # Voice Configuration
            voice_config = voice_setup.generate_voice_config(co, scraped_character_text)
            voice_setup.create_voice_script(character_path, voice_config)

            # Run Notebooks
            notebook_runner.run_notebooks()

    except Exception as e:
        logging.error(f"An error occurred in main: {e}")
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
