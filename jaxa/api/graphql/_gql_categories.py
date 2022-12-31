"""
Jira Xray API categories
"""


def load_query_from_file(path: str) -> str:
    with open(path) as f:
        return f.read()


class _MetaCategory:
    """Meta Category"""

    def __init__(self, session) -> None:
        self._session = session
