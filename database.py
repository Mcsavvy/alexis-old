from dataclasses import dataclass
from peewee import (
	SqliteDatabase,
	Model,
	CharField
)
from .config import DATABASE
import os


DB = SqliteDatabase(DATABASE)

class BaseModel(Model):
	class Meta:
		database = DB


class Sandbox(BaseModel):
	name = CharField(max_length=20, unique=True)
	host = CharField(max_length=50)
	username = CharField(max_length=20)
	password = CharField(max_length=50)

	def login(self):
		"""
		delt
		"""