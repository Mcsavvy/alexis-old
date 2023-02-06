import os
from dataclasses import dataclass
from typing import Callable, Optional, Type
from datetime import datetime
import config
import json
from logger import logger
from typedef import FileType, TimeStamp


def get_cache_hash(path: str) -> str:
	"""generate a unique hash for the cache
	
	NOTE: the hash should always be the same for the same <path>
	"""

	import hashlib

	return hashlib.sha1(path.encode("utf-8")).hexdigest()


def get_cache_location(hash: str) -> str:
	"""
	get the path where the cache would be stored

	Args:
		hash: the file's unique hash
	Returns: a path
	"""

	return os.path.join(config.CACHE_DIR, hash)


def get_metadata_location(hash: str) -> str:
	"""
	get the path where the metadata would be stored

	Args:
		hash: the file's unique hash
	"""

	return os.path.join(config.METADATA_DIR, hash + ".json")



class Metadata:
	"""This interface represents the metadata of a single cache file
	It provides methods for updating metadata.
	"""

	hash: str
	"a hash used to identify each file"

	origin: str
	"the absolute path to the original file on the remote server"

	name: str
	"the original file's name"

	created_at: TimeStamp
	"a timestamp showing when the cache was created"

	last_sync: TimeStamp
	"a timestamp showing when the cache was last synced"

	modified_at: TimeStamp
	"a timestamp showing when the cache was last modified"

	def __init__(self, cache: 'Cache', file: 'FileType'):
		"""
		initialize the metadata for a cache
		"""
		self.hash = cache.hash
		self.origin = file.path
		self.name = file.name
		location = get_metadata_location(cache.hash)

		file_stat = os.stat(cache.path)
		self.created_at = file_stat.st_ctime
		self.modified_at = file_stat.st_mtime

		if os.path.isfile(location):
			with open(location, 'r') as f:
				self.json = json.load(f)
			return
		self.last_sync = 0.0
		
	@property
	def json(self):
		"""
		return a json representaion of the metadata
		"""

		return dict(
			hash=self.hash, origin=self.origin, name=self.name,
			created_at=self.created_at, last_sync=self.last_sync,
			modified_at=self.modified_at
		)

	@json.setter
	def json(self, value: dict):
		"""
		update the metadata from a dictionary
		"""

		self.last_sync = value['last_sync']


	def save(self):
		"""
		write contents in metadata to a file
		"""
	
		location = get_metadata_location(self.hash)
		with open(location, "w+") as f:
			logger.debug("saving metadata for '%s' in '%s'", self.origin, location)
			json.dump(self.json, f)
		logger.debug("metadata saved")
		
	def update_sync(self, ts: Optional[TimeStamp] = None):
		"""
		update last_sync on the metadata. If ts(timestamp) is not
		provided, the current timestamp is used
		"""
		if ts:
			self.last_sync = ts
		else:
			self.last_sync = datetime.now().timestamp() - 0.001
	
	def update_modified(self, ts: Optional[TimeStamp] = None):
		"""
		update modified_at on the metadata. If ts(timestamp) is not
		provided, the current timestamp is used
		"""
		if ts:
			self.modified_at = ts
		else:
			self.modified_at = datetime.now().timestamp() - 0.001
	


class Cache:
	"""This interface represent a single cache file.
	It provides methods for interacting with a cache file.
	
	This interface is also able to propagate changes to the original file
	"""

	hash: str
	"a hash used to identify each file"

	meta: Metadata
	"cache metadata"

	path: str
	"absolute path to location where cache lives"

	name: str
	"the cache's name"

	file: 'FileType'
	"the cached file"

	def __init__(self, file: FileType):
		"""
		initialize a new cache object. this object could be for a new cache file
		or for an existing file.

		Args:
			file: a file object. this object represents the file to cache
		"""
		self.file = file
		self.hash = get_cache_hash(file.path)
		self.name = file.name
		self.path = get_cache_location(self.hash)
		logger.debug("cache '%s' for '%s'", self.hash, file.path)
		if os.path.isfile(self.path):
			logger.info("cache '%s' already exists", hash)
		else:
			logger.info("creating cache '%s'", self.hash)
			try:
				open(self.path, 'w+').close()
			except Exception as err:
				logger.error(err)
		self.meta = Metadata(self, file)
		

	def open(self):
		"""
		opens the cache and does syncing
		"""
		file_stat = self.file.stat()
		logger.debug("file stat: created = '%s', modified = '%s'",
					datetime.fromtimestamp(file_stat.st_ctime),
					datetime.fromtimestamp(file_stat.st_mtime))
		if self.meta.modified_at < file_stat.st_mtime:
			logger.info("origin newer, overwriting cache")
			self.write(self.file.read())
		elif self.meta.modified_at > file_stat.st_mtime:
			logger.info("cache newer, overwriting origin")
			self.file.write(self.read())
		self.meta.update_sync()
		self.meta.update_modified(self.meta.last_sync)
	

	def read(self, size: Optional[int]=None) -> str:
		"""read the contents of the cache.

		Args:
			size: the number of bytes to read from the cache
		
		Returns:
			The contents of the cache
		"""

		with open(self.path, "r") as cachefile:
			if size is not None:
				contents = cachefile.read(size)
			else:
				contents = cachefile.read()
		return contents

	def append(self, content: str):
		"""add new text to the cache without truncating
		the existing contents of the cache.
		All appended content would be added after the existing content
		in the file.

		Args:
			content: text to add to the file
		"""

		with open(self.path, "a") as cachefile:
			cachefile.write(content)
		self.meta.update_modified()
	
	def write(self, content: str):
		"""overwrite contents in cache with new content

		Args:
			content: text to write to the file
		"""

		with open(self.path, "w") as cachefile:
			cachefile.write(content)
		self.meta.update_modified()
