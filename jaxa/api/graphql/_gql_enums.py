"""Enums"""
from enum import auto
from strenum import LowercaseStrEnum


class GQLTransport(LowercaseStrEnum):
    requests = auto()
