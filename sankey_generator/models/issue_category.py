"""Model for an issue category."""

from typing import List


class IssueCategory:
    """Model for an issue category."""

    def __init__(self, name: str, sub_categories: List[str]):
        """Initialize the issue category."""
        self.name = name
        self.sub_categories = sub_categories
