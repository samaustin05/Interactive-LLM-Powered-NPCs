# modules/cohere_client.py
import cohere
import logging

class CohereClient:
    def __init__(self, api_key):
        try:
            self.client = cohere.Client(api_key)
            logging.info("Cohere client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Cohere client: {e}")
            raise

    def generate_text(self, prompt, max_tokens=2000, temperature=0.7, stop_sequences=None):
        try:
            response = self.client.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                k=0,
                p=0.75,
                frequency_penalty=0,
                presence_penalty=0,
                stop_sequences=stop_sequences or ["--"]
            )
            generated_text = response.generations[0].text.strip()
            logging.debug("Text generated successfully.")
            return generated_text
        except Exception as e:
            logging.error(f"Error generating text with Cohere: {e}")
            raise
