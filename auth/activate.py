"""
This file contains functions used to activate and deactivate sandboxes.

An active sandbox is the sandbox that is used when working with files
and running commands.

FUNCTIONS DECLARED
==================

get_active_sandbox(sandbox):
	this function gets the active sandbox

activate_sandbox(sandbox):
	this function activates the sandbox supplied

deactivate_sandbox():
	this function deactivates the active sandbox

switch_sandbox(sandbox):
	this function deactivates the active sandbox and activates
	the sandbox supplied
"""
from typing import Optional as O

from ..config import ACTIVE_SANDBOX_FILE
from ..database import DB, Sandbox
from ..logger import logger


def get_active_sandbox() -> O[Sandbox]:
    """
    gets the active sandbox

    Returns:
            The active sandbox or None if no sandbox is active
    """

    import os

    if not os.path.exists(ACTIVE_SANDBOX_FILE):
        logger.debug("active sandbox file %s missing", ACTIVE_SANDBOX_FILE)
        return None
    with open(ACTIVE_SANDBOX_FILE, "r") as sb:
        name = sb.readline().strip()
        if not name:
            logger.debug(
                "active sandbox file %r is empty, deleting...",
                ACTIVE_SANDBOX_FILE,
            )
            os.remove(ACTIVE_SANDBOX_FILE)
            return None
        logger.debug("read name %r from %s")
    with DB.atomic():
        query = Sandbox.select().where(Sandbox.name == name)
        if not query:
            logger.debug("could not find a sandbox name %r", name)
            logger.debug("deleting active sandbox file...")
            os.remove(ACTIVE_SANDBOX_FILE)
            return None
        return query.get()


def activate_sandbox(sandbox: Sandbox):
    """
    set sandbox as the active sandbox

    Args:
            sandbox: an instance of database.Sandbox
    """

    logger.debug("getting active sandbox...")
    active_sandbox = get_active_sandbox()
    if active_sandbox:
        logger.debug("active sandbox found")
        if sandbox == active_sandbox:
            logger.info("Sandbox is already active")
            return
    with open(ACTIVE_SANDBOX_FILE, "w+") as sb:
        logger.debug("writing %r into %s", sandbox.name, ACTIVE_SANDBOX_FILE)
        sb.write(sandbox.name)  # type: ignore
    logger.info("%r is now the active sandbox", sandbox.host)


def deactivate_sandbox():
    """
    deactivate the active sandbox
    """
    import os

    if not os.path.exists(ACTIVE_SANDBOX_FILE):
        logger.debug("active sandbox file %s missing", ACTIVE_SANDBOX_FILE)
    else:
        os.remove(ACTIVE_SANDBOX_FILE)
