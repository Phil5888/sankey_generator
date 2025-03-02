"""Model for a CSV filter."""


class CsvFilter:
    """Filter for a CSV file."""

    def __init__(self, target_label, column_name, values):
        """Initialize the filter."""
        self.target_label = target_label
        self.column_name = column_name
        self.values = values
