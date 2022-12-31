"""Enums"""
from enum import auto
from strenum import UppercaseStrEnum


class HTTPMethods(UppercaseStrEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
