import papermill as pm
import logging
from pathlib import Path
import json

class NotebookRunner:
    def __init__(self, config_file='config.json', notebooks_dir='notebooks', output_dir='notebooks_output'):
        """
        Initializes the NotebookRunner with directories and loads the configuration.

        Args:
            config_file (str): Path to the configuration file.
            notebooks_dir (str): Directory where the input notebooks are stored.
            output_dir (str): Directory where the executed notebooks will be saved.
        """
        self.config_file = config_file
        self.notebooks_dir = Path(notebooks_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load the config data from the JSON file
        self.config = self.load_config()

        # Map input to output notebooks
        self.notebook_files = {
            'create_character_vectordb.ipynb': 'executed_create_character_vectordb.ipynb',
            'create_face_recognition_representation.ipynb': 'executed_create_face_recognition_representation.ipynb',
            'create_public_vectordb.ipynb': 'executed_create_public_vectordb.ipynb'
        }

    def load_config(self):
        """
        Loads the configuration from the config file.

        Returns:
            dict: Configuration data.
        """
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                logging.info(f"Loaded config: {config}")
                return config
        except Exception as e:
            logging.error(f"Failed to load config file: {e}")
            raise

    def run_notebook(self, notebook, output_notebook):
        """
        Executes a single notebook.

        Args:
            notebook (str): Name of the input notebook.
            output_notebook (str): Name of the output notebook.
        """
        input_path = self.notebooks_dir / notebook
        output_path = self.output_dir / output_notebook

        logging.info(f"Executing notebook: {input_path}")
        logging.info(f"Output will be saved to: {output_path}")

        try:
            pm.execute_notebook(
                input_path=str(input_path),
                output_path=str(output_path)
            )
            logging.info(f"Successfully executed {notebook} and saved to {output_path}")
        except Exception as e:
            logging.error(f"Failed to execute {notebook}: {e}")
            raise

    def run_notebooks(self):
        """
        Executes all notebooks based on the loaded configuration.
        """
        game_name = self.config.get('game_name')
        characters = self.config.get('characters', [])

        for notebook, output_notebook in self.notebook_files.items():
            if 'character' in notebook and characters:
                for character in characters:
                    logging.info(f"Running {notebook} for character: {character['name']}")
                    self.run_notebook(notebook, output_notebook)
            else:
                logging.info(f"Running {notebook} for game: {game_name}")
                self.run_notebook(notebook, output_notebook)
