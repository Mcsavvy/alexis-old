"""
This module contains functions that complete the authentication
flow for login.
"""

import re
from typing import Callable
from typing import Optional as O
from typing import TypeVar

from rich import get_console
from rich.prompt import Prompt

from ..database import DB, Sandbox
from ..logger import logger
from .activate import activate_sandbox
from .common import (
    SSH_HOST_PATTERN,
    AuthState,
    has_internet_connection,
    verify_auth,
)
from .prompts import get_host, get_password, get_username
from .validators import (
    validate_host,
    validate_name,
    validate_password,
    validate_username,
)

console = get_console()


def add_sandbox(host: str, username: str, password: str, name: O[str]):
    """
    add sandbox to database. it optionally sets the sandbox as the active
    sandbox.

    Args:
            host: sandbox host
            username: sandbox username
            password: sandbox password
    """
    default = ""
    sandboxes = Sandbox.select()
    logger.debug("%d sandboxes found in database", sandboxes.count())
    if not sandboxes:
        if sandboxes.where(Sandbox.name == "default"):
            logger.debug("sandbox with name 'default' was found.")
        else:
            default = "default"
    if not default:
        hostname = SSH_HOST_PATTERN.match(host)["hostname"]  # type: ignore
        if sandboxes.where(Sandbox.name == host):
            logger.debug("sandbox with name '%s' was found.", host)
            default = ...
        else:
            default = hostname
    while not validate_name(name):
        name = Prompt.ask(
            "suggest a nice short name for this sandbox", default=default
        )  # type: ignore
    new = Sandbox.create(
        name=name, host=host, username=username, password=password
    )
    new.save()
    logger.info("%s (%s) successfully logged in", host, name)
    return new


def is_logged_in(host: str):
    """
    Verify if a sandbox is logged in

    Args:
        host: sandbox host

    Returns: True if sandbox is logged in else False
    """
    with DB.atomic():
        if Sandbox.select().where(Sandbox.host == host):
            return True
    return False



def login(
    host: O[str] = "",
    username: O[str] = "",
    password: O[str] = "",
    name: O[str] = "",
    activate: O[bool] = None,
):
    """Initiate sandbox login.

    Returns: True if sandbox was connect to, else False
    """

    host_match: re.Match[str]

    if not has_internet_connection():
        logger.critical("no internet connection!")
        return False

    if host:
        if not validate_host(host):
            return None
    if username:
        if not validate_username(username):
            return None
    if password:
        if not validate_password(password):
            return None

    while True:
        if not (host or (host := get_host())):
            continue
        host_match = SSH_HOST_PATTERN.match(host)  # type: ignore
        if not (username
            or (username := get_username(default=host_match["username"]))):
            continue
        if not (password or (password := get_password())):
            continue
        break

    if is_logged_in(host):
        logger.warning("sandbox is already logged in ⚠")
        return False
    
    # verify authentication...
    status = verify_auth(host, username, password)
    if status is AuthState.FAILURE:
        logger.warning("username or password is incorrect ❎")
        logger.info("sandbox may also be asleep 💤")
        return False
    elif status is AuthState.BADHOST:
        logger.warning("sandbox was not found 🍃")
        return False
    
    # add sandbox to database
    new = add_sandbox(host, username, password, name)

    # activate sandbox?
    if activate is None:
        activate = (True
            if Sandbox.select().count() == 1
            else bool(Prompt.ask(
                f"set [b cyan]{name}[/] as active sandbox?", default=True
            )))
    if activate:
        logger.info("activating sandbox [b cyan]%s[/]", name)
        activate_sandbox(new)


def logout(host: str):
    """
    logout from a sandbox

    Args:
        host: sandbox host

    Return: nothing
    """

    if not is_logged_in(host):
        return False

    with DB.atomic():
        sandbox = Sandbox.select().where(Sandbox.host == "")
    