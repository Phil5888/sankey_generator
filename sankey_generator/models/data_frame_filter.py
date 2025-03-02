"""Filter for data frame."""


class DataFrameFilter:
    """Filter for a data frame."""

    def __init__(self, column: str, values: list[str]):
        """Initialize the filter."""
        self.column = column
        self.values = values
