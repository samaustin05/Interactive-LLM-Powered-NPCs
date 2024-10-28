# modules/file_ops.py
import json
import logging
from pathlib import Path

class FileOperations:
    def __init__(self):
        pass

    def write_text_file(self, file_path, content):
        """
        Writes text content to a file.

        Args:
            file_path (str or Path): The path to the file.
            content (str): The text content to write.
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Wrote text file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to write text file {file_path}: {e}")
            raise

    def write_json_file(self, file_path, data):
        """
        Writes JSON data to a file.

        Args:
            file_path (str or Path): The path to the JSON file.
            data (dict): The JSON data to write.
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Wrote JSON file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to write JSON file {file_path}: {e}")
            raise

    def read_text_file(self, file_path):
        """
        Reads text content from a file.

        Args:
            file_path (str or Path): The path to the file.

        Returns:
            str: The content of the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logging.info(f"Read text file: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Failed to read text file {file_path}: {e}")
            raise

    def read_json_file(self, file_path):
        """
        Reads JSON data from a file.

        Args:
            file_path (str or Path): The path to the JSON file.

        Returns:
            dict: The JSON data.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.info(f"Read JSON file: {file_path}")
            return data
        except Exception as e:
            logging.error(f"Failed to read JSON file {file_path}: {e}")
            raise
