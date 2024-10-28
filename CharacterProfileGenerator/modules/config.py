# modules/config.py
import json
from pathlib import Path
import logging

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.data = json.load(f)
            
    def load_config(self):
        try:
            with self.config_path.open('r', encoding='utf-8') as f:
                config = json.load(f)
            logging.info(f"Configuration loaded from {self.config_path}.")
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_path} not found.")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {self.config_path}: {e}")
            raise
