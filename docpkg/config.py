"""This module contains the configuration routines."""

from typing import Optional, TypeVar

T = TypeVar('T')


class MyConfig:
    """Loads and manages the configuration.

    Args:
        filename: The filename to load configs from.

    """

    def __init__(self, filename: str) -> None:
        pass

    def get_option(self, name: str, default: Optional[T] = None) -> T:
        """Returns the requested option from the loaded configs.

        :param name: The option name to get.
        :param default: The default to return, if the option was not found
                        in the configs.

        """
        pass
