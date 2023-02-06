from cache import CacheFile as cache
import os
from config import CACHE_DIR, CHECKPOINT_DIR, METADATA_DIR
from logger import logger


def setup():
	if not os.path.exists(CACHE_DIR):
		logger.debug("creating cache directory")
		os.mkdir(CACHE_DIR)
	if not os.path.exists(METADATA_DIR):
		logger.debug("creating metadata directory")
		os.mkdir(METADATA_DIR)
	if not os.path.exists(CHECKPOINT_DIR):
		logger.debug("creating checkpoint directory")
		os.mkdir(CHECKPOINT_DIR)