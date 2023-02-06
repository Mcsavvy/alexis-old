import re
import socket
from enum import Enum
from typing import Callable
from typing import Optional as O
from typing import TypeVar

from rich import get_console
from rich.prompt import Prompt

from ..config import ACTIVE_SANDBOX_FILE
from ..database import Sandbox
from ..logger import logger

SSH_HOST_PATTERN = re.compile(
    r"(?P<username>[a-z0-9]*).(?P<hostname>[a-z0-9]*).alx-cod.online"
)

T = TypeVar("T")
PromptT = O[Callable[[], O[str]]]
console = get_console()


class AuthState(Enum):
    """Different Authentication states

    * SUCCESS: Authentication was successful
    * FAILURE: Host was found but authentication failed
    * BADHOST: Host was not found
    """

    SUCCESS = 0
    FAILURE = 1
    BADHOST = 2


def has_internet_connection() -> bool:
    """
    Test if internet connection is available by pinging a website.

    Returns:
            True if there is network connection, False otherwise.
    """
    import requests

    with console.status("checking internet connection...") as status:
        try:
            logger.debug("pinging 8.8.8.8")
            requests.get("https://8.8.8.8")
            logger.debug("ping was successful")
            status.update("internet connection ✔")
            return True
        except requests.exceptions.ConnectionError:
            logger.debug("ping failed")
            status.update("no internet connection ⚠")
            return False


def verify_auth(host: str, username: str, password: str) -> AuthState:
    """
    Test if ssh host can be connected to using the credentials supplied.
    This is often used to confirm if the user supplied correct details or is
    the sandbox isn't asleep.

    Args:
            host: sandbox hostname
            username: sandbox username
            password: sandbox password

    Returns: An authentication state, could be one of:
            * `AuthState.FAILURE`: bad credentials
            * `AuthState.SUCCESS`: authentication was successfule
            * `AuthState.BADHOST`: host not known
    """

    from paramiko import AuthenticationException, AutoAddPolicy, SSHClient

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    try:
        with console.status(f"authenticating to [b cyan]{host}[/]..."):
            client.connect(
                hostname=host,
                username=username,
                password=password,
                look_for_keys=False,
            )
    except AuthenticationException as e:
        return AuthState.FAILURE
    except socket.gaierror as e:
        return AuthState.BADHOST
    return AuthState.SUCCESS
