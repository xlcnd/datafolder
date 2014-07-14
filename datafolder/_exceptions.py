# -*- coding: utf-8 -*-

"""Exceptions for 'datafolder' package."""


class DataFolderException(Exception):

    """Base exception for 'datafolder' package.

    Should't NOT be raised directly, but can be used as a
    catch-all exception for the package.

    """


class DataFolderNotFoundError(DataFolderException):

    """Exception to be raised when the data folder is not found."""
