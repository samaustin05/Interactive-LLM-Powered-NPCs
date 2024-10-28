# modules/voice_setup.py
import json
import logging
from modules.file_ops import FileOperations
from modules.utils import generate_json

class VoiceSetup:
    def __init__(self):
        self.file_ops = FileOperations()

    def generate_voice_config(self, co, character_text):
        prompt = (
            "Based on the following character information, generate a voice configuration in valid JSON format. "
            "The JSON should include the following keys: 'voice_type', 'pitch', 'speed', and 'tone'. "
            "Ensure that all strings are properly quoted and that the JSON is complete and free of syntax errors.\n\n"
            "Example Output:\n"
            "```json\n"
            "{\n"
            '  "voice_type": "male",\n'
            '  "pitch": "medium",\n'
            '  "speed": "normal",\n'
            '  "tone": "calm"\n'
            "}\n"
            "```\n\n"
            f"{character_text}"
        )
        schema = {
            "type": "object",
            "properties": {
                "voice_type": {"type": "string"},
                "pitch": {"type": "string"},
                "speed": {"type": "string"},
                "tone": {"type": "string"}
            },
            "required": ["voice_type", "pitch", "speed", "tone"]
        }
        try:
            voice_config = generate_json(
                co=co,
                prompt=prompt,
                schema=schema,
                retries=3,
                delay=2,
                max_tokens=300,
                temperature=0.7,
                stop_sequences=["```"]
            )
            return voice_config
        except Exception as e:
            logging.error(f"Failed to generate voice configuration: {e}")
            raise

    def create_voice_script(self, character_path, voice_config):
        try:
            voice_config_path = character_path / 'voice_config.json'
            self.file_ops.write_json_file(voice_config_path, voice_config)
            logging.info(f"Wrote voice configuration file: {voice_config_path}")
        except Exception as e:
            logging.error(f"Error writing voice configuration JSON: {e}")
            raise
