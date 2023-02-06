from abc import ABC, abstractmethod, abstractproperty

TimeStamp = float

class StatType(ABC):
	@property
	@abstractmethod
	def st_ctime(self) -> TimeStamp:
		"""the time the file was created"""

	@property
	@abstractmethod
	def st_mtime(self) -> TimeStamp:
		"""the time the file was last modified"""

class FileType(ABC):
	@property
	@abstractmethod
	def name(self) -> str:
		"""the name of the file"""

	@property
	@abstractmethod
	def path(self) -> str:
		"""the absolute path of this file"""

	@abstractmethod
	def __enter__(self):
		"""
		allows use of object as context manager.
		used to open file for I/O operations
		"""

	@abstractmethod
	def __exit__(self):
		"""
		allows use of objects as context manager.
		used to close file after I/O operations
		"""

	@abstractmethod
	def open(self):
		"""
		used to open file for I/O operations
		"""

	@abstractmethod
	def close(self):
		"""
		used to close file after I/O operations
		"""

	@abstractmethod
	def stat(self) -> StatType:
		"""
		Returns:
			an object containing file information.
			the object must have st_mtime and st_ctime attributes.
		"""
	
	@abstractmethod
	def readable(self) -> bool:
		"""
		Returns: True if file can be read from, False otherwise.
		"""

	@abstractmethod
	def writable(self) -> bool:
		"""
		Returns: True if a file can be written to
		"""

	@abstractmethod
	def read(self, size: int=...) -> str:
		"""
		read `size` bytes from the file. If `size` is negative, all contents
		should be read.

		Returns: contents read from the file
		"""

	@abstractmethod
	def write(self, data: 'str | bytes'):
		"""
		write `data` to the file.
		"""
	