# modules/logger.py
import logging
from pathlib import Path

def setup_logging(log_file='logs/main.log'):
    Path('logs').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,  # Set to DEBUG for detailed logs
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)  # Set to INFO for console
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("Logging is set up.")
