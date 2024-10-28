# generation.py

import json
import logging
import time
from jsonschema import validate, ValidationError
from .utils import clean_json, ensure_complete_text

def validate_json(data, schema):
    """
    Validates JSON data against a provided schema.
    """
    try:
        validate(instance=data, schema=schema)
        logging.info("JSON schema validation passed.")
    except ValidationError as ve:
        logging.error(f"JSON schema validation error: {ve}")
        raise

def generate_json(co, prompt, schema, retries=3, delay=2, max_tokens=1000, temperature=0.7, stop_sequences=["```"]):
    """
    Generates and validates JSON using Cohere's API with retry mechanism.
    """
    for attempt in range(1, retries + 1):
        try:
            generated_text = co.generate_text(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop_sequences=stop_sequences
            )
            cleaned_text = clean_json(generated_text)
            logging.debug(f"Attempt {attempt} - Generated JSON Text:\n{cleaned_text}")

            parsed_json = json.loads(cleaned_text)
            validate_json(parsed_json, schema)

            logging.info("JSON generated and validated successfully.")
            return parsed_json

        except (json.JSONDecodeError, ValidationError) as e:
            logging.error(f"Attempt {attempt}: Error - {e}")
            logging.debug(f"Raw JSON Text:\n{cleaned_text[:500]}")  # Log first 500 chars
            # Save the problematic JSON for manual inspection
            with open(f'logs/problematic_json_attempt_{attempt}.json', 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            if attempt < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("All retry attempts failed.")
                raise

def generate_text(co, prompt, schema=None, retries=3, delay=2, max_tokens=1000, temperature=0.7, stop_sequences=None):
    """
    General text generation function with optional schema validation.
    """
    for attempt in range(1, retries + 1):
        try:
            generated_text = co.generate_text(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop_sequences=stop_sequences
            )
            complete_text = ensure_complete_text(co, generated_text, "Please continue the text.")
            logging.debug(f"Attempt {attempt} - Generated Text Length: {len(complete_text)} characters.")
            return complete_text

        except Exception as e:
            logging.error(f"Attempt {attempt}: Error - {e}")
            if attempt < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("All retry attempts failed.")
                raise
