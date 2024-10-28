# modules/utils.py
import re
import json
import logging
import time
from jsonschema import validate, ValidationError

def clean_json(text):
    """
    Cleans the generated JSON text by removing code block markers,
    ensuring it ends with a closing brace or bracket, and removing trailing commas.

    Args:
        text (str): The raw JSON string.

    Returns:
        str: The cleaned JSON string.
    """
    text = re.sub(r'```json', '', text)
    text = re.sub(r'```', '', text)
    text = text.strip()

    # Ensure JSON ends properly
    if not (text.endswith('}') or text.endswith(']')):
        text += '}'

    # Remove trailing commas before closing braces/brackets
    text = re.sub(r',\s*([}\]])', r'\1', text)

    return text

def validate_json(data, schema):
    """
    Validates JSON data against a provided schema.

    Args:
        data (dict): The JSON data to validate.
        schema (dict): The JSON schema to validate against.

    Raises:
        ValidationError: If the JSON data does not conform to the schema.
    """
    try:
        validate(instance=data, schema=schema)
        logging.info("JSON schema validation passed.")
    except ValidationError as ve:
        logging.error(f"JSON schema validation error: {ve}")
        raise

def generate_json(co, prompt, schema, retries=3, delay=2, max_tokens=1000, temperature=0.7, stop_sequences=["```"]):
    """
    Generates and validates JSON using Cohere's API with a retry mechanism.

    Args:
        co (CohereClient): The Cohere API client instance.
        prompt (str): The prompt to send to Cohere for generation.
        schema (dict): The JSON schema to validate the generated JSON against.
        retries (int, optional): Number of retry attempts. Defaults to 3.
        delay (int, optional): Delay in seconds between retries. Defaults to 2.
        max_tokens (int, optional): Maximum tokens for the generation. Defaults to 2000.
        temperature (float, optional): Sampling temperature. Defaults to 0.7.
        stop_sequences (list, optional): Sequences that indicate stopping. Defaults to ["```"].

    Returns:
        dict: The validated JSON data.

    Raises:
        Exception: If all retry attempts fail.
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
            # Attempt to log a snippet of the problematic JSON if available
            if 'cleaned_text' in locals():
                logging.debug(f"Raw JSON Text:\n{cleaned_text[:500]}")  # Log first 500 chars
            if attempt < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("All retry attempts failed.")
                raise

def ensure_complete_text(co, text, prompt_continuation, max_tokens=150):
    """
    Ensures that the generated text is complete by checking its ending and requesting continuation if necessary.

    Args:
        co (CohereClient): The Cohere API client instance.
        text (str): The generated text.
        prompt_continuation (str): The prompt to generate continuation.
        max_tokens (int, optional): Maximum tokens for the continuation. Defaults to 150.

    Returns:
        str: The complete text.
    """
    logging.debug("Checking if the generated text is complete.")
    if text.endswith(('.', '!', '?')):
        logging.debug("Text is complete.")
        return text
    logging.debug("Text is incomplete. Generating continuation.")
    continuation = co.generate_text(prompt_continuation, max_tokens=max_tokens)
    complete_text = text + ' ' + continuation
    logging.debug("Completed text generation after continuation.")
    return complete_text