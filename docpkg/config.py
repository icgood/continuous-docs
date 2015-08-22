

"""This module contains the configuration routines."""


class MyConfig(object):
    """Loads and manages the configuration.

    :param filename: The filename to load configs from.

    """

    def __init__(self, filename):
        pass

    def get_option(self, name, default=None):
        """Returns the requested option from the loaded configs.

        :param name: The option name to get.
        :param default: The default to return, if the option was not found
                        in the configs.

        """
        pass


# vim:et:fdm=marker:sts=4:sw=4:ts=4
