import logging
from src.core.config import config

# Logging Configuration
logging.basicConfig(
    level=getattr(logging, config.log_level.upper()),
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Configure uvicorn to be quieter
for uvicorn_logger in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
    logging.getLogger(uvicorn_logger).setLevel(logging.WARNING)