from . import (
	DB, Sandbox, login, config,
	logger
)
import os
import errno
from .cli import main


# create cache directory
logger.debug("creating cache directory...")
if os.path.exists(config.CACHE_DIR):
	logger.debug("%s exists", config.CACHE_DIR)
	if not os.path.isdir(config.CACHE_DIR):
		logger.critical(
			"cache directory path %s already exists but is not a directory.",
			config.CACHE_DIR
		)
		exit(errno.EEXIST)
else:
	try:
		os.makedirs(config.CACHE_DIR)
	except PermissionError:
		logger.critical("not enough permissons to create cache directory %s",
			config.CACHE_DIR)
		exit(errno.EACCES)
	logger.debug("created cache directory")

# create metadata directory
logger.debug("creating metadata directory...")
if os.path.exists(config.METADATA_DIR):
	logger.debug("%s exists", config.METADATA_DIR)
	if not os.path.isdir(config.METADATA_DIR):
		logger.critical(
			"metadata directory path %s already exists but is not a directory.",
			config.METADATA_DIR
		)
		exit(errno.EEXIST)
else:
	try:
		os.makedirs(config.METADATA_DIR)
	except PermissionError:
		logger.critical("not enough permissons to create metadata directory %s",
			config.METADATA_DIR)
		exit(errno.EACCES)
	logger.debug("created metadata directory")


# create data directory
logger.debug("creating data directory...")
if os.path.exists(config.DATA_DIR):
	logger.debug("%s exists", config.DATA_DIR)
	if not os.path.isdir(config.DATA_DIR):
		logger.critical(
			"data directory path %s already exists but is not a directory.",
			config.DATA_DIR
			)
		exit(errno.EEXIST)
else:
	try:
		os.makedirs(config.DATA_DIR)
	except PermissionError:
		logger.critical("not enough permissons to create data directory %s",
			config.DATA_DIR)
		exit(errno.EACCES)
	logger.debug("created data directory")


# create database
logger.debug("creating database...")
if os.path.exists(config.DATABASE):
	logger.debug("%s exists", config.DATABASE)
	if not os.path.isfile(config.DATABASE):
		logger.critical(
			"database %s already exists but is not a file.",
			config.CACHE_DIR
		)
		exit(errno.EEXIST)
else:
	try:
		logger.debug("creating directory %s if it doesn't exist...", 
					os.path.dirname(config.DATABASE))
		os.makedirs(os.path.dirname(config.DATABASE), exist_ok=True)
		logger.debug("creating database %s...", config.DATABASE)
		open(config.DATABASE, "w+").close()
		logger.debug("connecting to database...")
		DB.connect()
		logger.debug("creating database tables...")
		DB.create_tables([Sandbox])
		logger.debug("closing database")
		DB.close()
		logger.debug("created database")
	except PermissionError:
		logger.critical("not enough permissons to create cache directory %s",
			config.CACHE_DIR)
		exit(errno.EACCES)

main()