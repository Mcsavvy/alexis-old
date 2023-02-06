import configparser
from os import getenv, path

from paramiko import AutoAddPolicy, SSHClient

from constants import *
from error import ConfigNotFound


def get_config(config: configparser.ConfigParser, section: str,
		name: str, env: str) -> str:
	try:
		value = config.get(section, name)
	except configparser.NoOptionError:
		value = getenv(env)
	if not value:
		raise ConfigNotFound(
			"config.ini", section, name, env)
	return value



config = configparser.ConfigParser()
config.read("config.ini")
host = get_config(config, "ssh", "host", SSH_HOST_KEY)
username = get_config(config, "ssh", "username", SSH_USERNAME_KEY)
password = get_config(config, "ssh", "password", SSH_PASSWORD_KEY)
basedir = get_config(config, "sftp", "basedir", SANDBOX_BASEDIR_KEY)

print("ssh {}@{}".format(username, host))
print("password:", password)
