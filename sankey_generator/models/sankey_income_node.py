"""Root node for income."""

from sankey_generator.models.sankey_node import SankeyNode


class SankeyIncomeNode:
    """Root node for income."""

    def __init__(self, label, incomeNodes: list[SankeyNode]):
        """Initialize the income node."""
        self.label: str = label
        self.incomeNodes: list[SankeyNode] = incomeNodes
        self.issueNodes: list[SankeyNode] = []

    def add_issue(self, child):
        """Add an issue to the income node."""
        self.issueNodes.append(child)

    def get_issues_amount(self):
        """Get the total amount of issues."""
        return sum([child.amount for child in self.issueNodes])

    def get_income_amount(self):
        """Get the total amount of income."""
        return sum([parent.amount for parent in self.incomeNodes])
