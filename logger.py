import logging
import os
from pathlib import Path

import config

LOG_DIR = Path(config.LOG_DIR)
LOG_FILE = LOG_DIR / 'app.log'
LOG_LEVEL = config.LOG_LEVEL

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
