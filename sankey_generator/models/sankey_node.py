"""Model for a Sankey node."""

from sankey_generator.models.csv_filter import CsvFilter


class SankeyNode:
    """Model for a Sankey node."""

    def __init__(self, amount, label, csv_filter: CsvFilter):
        """Initialize the Sankey node."""
        self.amount = amount
        self.label = label
        self.childNodes = []
        self.csv_filter = csv_filter

    def add_child(self, child):
        """Add a child to the Sankey node."""
        self.childNodes.append(child)
