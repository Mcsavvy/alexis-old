import os
import pathlib


BASE_DIR = os.path.dirname(__file__)
'''Base directory where all cache and metadata files would live.
It's important that the contents in this directory are not modified
unless you know what you're doing ;)

Defaults to the package's directory'''

METADATA_DIR = os.path.join(BASE_DIR, ".metadata")
"A directory where metadata files would live"

CACHE_DIR = os.path.join(BASE_DIR, ".cache")
"The directory where cache files would live"

CHECKPOINT_DIR = os.path.join(BASE_DIR, ".checkpoints")
"The directory where checkpoint files would live"

DATA_DIR = os.path.join(BASE_DIR, ".data")
"The directory where application data would be kept"

ACTIVE_SANDBOX_FILE = os.path.join(DATA_DIR, "sb")
"The file where information about the active sandbox is kept"

DATABASE = os.path.join(DATA_DIR, "alexis.sql")
"Path to database"

DEBUG_MODE_ON = False
"Toggle application debug mode"

LOG_LEVEL = 20 # INFO
"Application log level"

if DEBUG_MODE_ON:
	LOG_LEVEL = 10 # DEBUG


LOG_FORMAT = "%(message)s"
"Logger message format"