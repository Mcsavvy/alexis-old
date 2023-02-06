from typing import Any
from typing import Optional as O

from ..database import DB, Sandbox
from ..logger import logger
from .common import SSH_HOST_PATTERN


def validate_host(host: Any) -> bool:
    """
    validate sandbox host

    Args:
            host: sandbox host
    Returns: True if validated else False
    """

    if not host:
        logger.warning("Sandbox box host cannot be left blank!")
        return False
    host_match = SSH_HOST_PATTERN.match(host)  # type: ignore
    if not host_match:
        logger.warning(
            (
                f"'{host}' doesn't look like a valid ALX sandbox host\n"
                "sample ➜ [bold cyan]d5f37ec849f8.05d11b28.alx-cod.online[/]"
            )
        )
        return False
    return True


def validate_username(username: Any) -> bool:
    """
    validate sandbox username

    Args:
            username: sandbox username
    Returns: True if validated else False
    """
    if not username:
        logger.warning("sandbox username cannot be left blank!")
        return False
    return True


def validate_password(password: Any) -> bool:
    """
    validate sandbox username

    Args:
            username: sandbox username
    Returns: True if validated else False
    """
    if not password:
        logger.warning("sandbox password cannot be left blank!")
        return False
    return True


def validate_name(name: Any) -> bool:
    """
    validate sandbox name

    Args:
            name: sandbox name
    Returns: True if validated else False
    """
    if not (isinstance(name, str) or name):
        logger.warning("sandbox name cannot be left blank!")
        return False
    with DB.atomic():
        if Sandbox.select().where(Sandbox.name == name).exists():
            logger.warning("sandbox name %s already exists", name)
            return False
    return True
