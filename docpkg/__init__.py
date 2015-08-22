

"""This is the base package for ``docpkg``. It really only contains the base
exception for the package.

"""

class DocpkgError(Exception):
    """The base error for the package. All custom exceptions raised will derive
    from this exception.

    """
    pass


# vim:et:fdm=marker:sts=4:sw=4:ts=4
