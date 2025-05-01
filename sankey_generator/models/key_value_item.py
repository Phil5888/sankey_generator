"""Filter item model for Sankey generator. This is a data transfer object for the config window to add or edit an item."""


class KeyValueItem:
    """Class representing a filter item."""

    def __init__(self, key: str, value: list[str]):
        """Initialize the filter item."""
        self.key = key
        self.value = value
