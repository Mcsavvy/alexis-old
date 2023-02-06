import click
from .auth import (
	login as _login,
	is_logged_in
)
from rich.prompt import Prompt
from .database import DB, Sandbox
from .logger import logger


@click.group()
def main():
	"""
	Alexis Command Line Controller.
	"""


@main.command()
@click.option("--host", "-h", help="ALX sandbox host")
@click.option("--username", "-u", help="ALX sandbox username")
@click.option("--password", "-p", help="ALX sandbox password")
@click.option("--name", "-n", help="a short name for the sandbox")
def login(host, username, password, name):
	"""
	login into an ALX sandbox
	"""
	_login(host, username, password, name)


@main.command()
@click.option("--host", "-h", help="ALX sandbox host to logout from")
@click.option("--name", "-h", help="Shortname of sandbox to logout from")
@click.option("--yes" "-y", "confirm",help="are you sure you wqant to logout?")
def logout(host, name, confirm):
	"""
	logout from an ALX sandbox
	"""

	if name and not host:
		with DB.atomic():
			if (sandbox:= Sandbox.select().where(Sandbox.name == name)):
				host = sandbox.host
			else:
				raise click.Abort(f"no sandbox named '{host}'")
	else:
		name = None
	if not confirm:
		confirm = Prompt.ask(
			f"are you sure you want to logout from [b cyan]{host}[/]?",
			default=True)
	if not is_logged_in(host):
		if name:
			raise click.Abort(f"sandbox '{name}' is not logged in")
		raise click.Abort(f"sandbox '{host}' is not logged in")
	logger.debug("logging out...")
	