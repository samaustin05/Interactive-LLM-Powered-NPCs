# modules/image_handler.py
import shutil
import logging
from pathlib import Path
import requests
from PIL import Image, UnidentifiedImageError 

class ImageHandler:
    def __init__(self, serpapi_api_key):
        """
        Initializes the ImageHandler with the provided SerpAPI API key.

        Args:
            serpapi_api_key (str): Your SerpAPI API key.
        """
        self.serpapi_api_key = serpapi_api_key
        self.last_valid_image = None  # Store the path of the last valid image

    def add_character_images(self, character_path, image_sources):
        images_path = character_path / 'images'
        images_path.mkdir(parents=True, exist_ok=True)

        try:
            # If image_sources is empty, fetch images using SerpAPI
            if not image_sources:
                logging.info("No image sources provided. Fetching images from SerpAPI.")
                image_sources = self.fetch_images_from_serpapi(character_path.stem, num_images=5)

            added_images = 0  # Track how many valid images are added
            for idx, img_url in enumerate(image_sources, start=1):
                if not img_url:
                    logging.warning(f"No URL found for image {idx}. Skipping.")
                    continue

                img_dest = images_path / f'{idx}.jpg'
                try:
                    self.download_image(img_url, img_dest)
                    logging.info(f"Downloaded image {img_url} to {img_dest}.")
                    added_images += 1
                except Exception as e:
                    logging.error(f"Failed to download image from {img_url}: {e}")

            # If no valid images were added, generate placeholders
            if added_images == 0:
                logging.warning(f"No valid images found. Generating placeholder images for {character_path.name}.")
                self.generate_placeholder_images(images_path)

            logging.info(f"Added {added_images} images for {character_path.name}.")

            # Now create test.jpg from the first valid character image
            self.create_test_image(character_path.stem, images_path)

        except Exception as e:
            logging.error(f"Error adding images for {character_path.name}: {e}")
            raise


    def fetch_images_from_serpapi(self, character_name, num_images=5):
        """
        Fetches image URLs from SerpAPI based on the character's name with enhanced query.

        Args:
            character_name (str): Name of the character.
            num_images (int): Number of image URLs to fetch.

        Returns:
            list: List of image URLs.
        """
        # Enhanced query to fetch front-facing images
        query = f"{character_name} front view portrait"
        logging.info(f"Fetching images with query: {query}")

        search_url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "tbm": "isch",
            "q": query,
            "num": num_images,
            "ijn": "0",
            "api_key": self.serpapi_api_key,
            "safe": "active",  # Enable safe search
        }

        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "images_results" not in data:
                logging.warning(f"No image results found for query: {query}")
                return []

            image_urls = [img["original"] for img in data["images_results"][:num_images]]
            logging.info(f"Fetched {len(image_urls)} image URLs from SerpAPI for query: {query}")
            return image_urls

        except requests.exceptions.RequestException as e:
            logging.error(f"SerpAPI request failed: {e}")
            return []

    def download_image(self, url, dest_path):
        """Downloads and validates an image from the given URL. 
        If the download fails, the previous valid image is copied instead."""
        try:
            response = requests.get(url, stream=True, timeout=10)  # Add a timeout
            response.raise_for_status()  # Ensure the request was successful

            with open(dest_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            # Validate the downloaded image
            with Image.open(dest_path) as img:
                img.verify()  # Verify the image integrity

            # If successful, update the last valid image
            self.last_valid_image = dest_path
            logging.info(f"Downloaded and verified image from {url}.")

        except (requests.exceptions.RequestException, UnidentifiedImageError, OSError) as e:
            logging.error(f"Failed to download or verify image from {url}: {e}")

            # Use the last valid image as a fallback
            if self.last_valid_image and self.last_valid_image.exists():
                shutil.copy(self.last_valid_image, dest_path)
                logging.info(f"Copied fallback image from {self.last_valid_image} to {dest_path}.")
            else:
                logging.warning("No valid fallback image available. Skipping this image.")

    def generate_placeholder_images(self, images_path, count=5):
        """Generate placeholder images if no images are provided or found."""
        try:
            for i in range(1, count + 1):
                placeholder_img = Image.new('RGB', (300, 300), color=(73, 109, 137))
                placeholder_img_path = images_path / f'{i}.jpg'
                placeholder_img.save(placeholder_img_path)
                logging.info(f"Generated placeholder image: {placeholder_img_path}")
        except Exception as e:
            logging.error(f"Error generating placeholder images: {e}")
            raise

    def create_test_image(self, character_name, images_path):
        """Creates a test.jpg in the project root from the first valid character image."""
        try:
            root_path = Path.cwd()  # Project root directory
            test_img_path = root_path / 'test.jpg'  # Path for the test image

            # Use the first valid image if available
            character_images = list(images_path.glob("*.jpg"))
            if character_images:
                shutil.copy(character_images[0], test_img_path)
                logging.info(f"Copied {character_images[0]} as test.jpg in the project root.")
            else:
                # Fallback to generating a red placeholder image if no valid images
                test_img = Image.new('RGB', (300, 300), color=(255, 0, 0))
                test_img.save(test_img_path)
                logging.info(f"Generated red placeholder test.jpg at: {test_img_path}")

        except Exception as e:
            logging.error(f"Error creating test.jpg: {e}")
            raise