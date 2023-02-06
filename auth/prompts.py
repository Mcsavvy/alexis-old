from typing import Optional as O

from rich.prompt import Prompt

from ..logger import logger
from .validators import validate_host, validate_password, validate_username


def get_host(default: str = ..., msg: str = ...):
    """
    prompt user for sandbox host
    """

    if not msg or msg is ...:
        msg = "please your sandbox host"

    host = Prompt.ask(msg, default=default)
    if not validate_host(host):
        return None
    return host


def get_username(default: str = ..., msg: str = ...):
    """
    prompt user for sandbox username
    """

    if not msg or msg is ...:
        msg = "enter sandbox username"

    username = Prompt.ask(msg, default=default)
    if not validate_username(username):
        return None
    return username


def get_password(default: str = ..., msg1: str = ..., msg2: str = ...):
    """
    prompt user for sandbox password
    """

    if not msg1 or msg1 is ...:
        msg1 = "enter sandbox password"
    if not msg1 or msg1 is ...:
        msg1 = "enter sandbox password again"

    password1 = Prompt.ask(msg1, default=default)
    if not validate_password(password1):
        return None
    if default != ... and password1 == default:
        return password1
    password2 = Prompt.ask(msg2, default=default)
    if password1 != password2:
        logger.warning("passwords dont match!")
        return None
    return password1
