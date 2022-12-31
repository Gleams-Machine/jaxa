"""Exceptions"""


class APIError(Exception):
    """Base Exception"""


class StatusCodeError(APIError):
    """Status code Exception"""
