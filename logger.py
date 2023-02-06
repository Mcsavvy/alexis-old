import logging
from .config import DEBUG_MODE_ON, LOG_FORMAT, LOG_LEVEL
from rich.logging import RichHandler

handler = RichHandler(
	show_time=False,
	show_level=DEBUG_MODE_ON,
	show_path=DEBUG_MODE_ON,
	rich_tracebacks=True,
	tracebacks_show_locals=DEBUG_MODE_ON,
	markup=True
)

logging.basicConfig(
	format=LOG_FORMAT,
	datefmt="[%X]",
	handlers=[handler]
)
logger = logging.getLogger("alexis")
logger.setLevel(LOG_LEVEL)