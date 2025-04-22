"""Root node for income."""

from sankey_generator.models.sankey_node import SankeyNode


class SankeyRootNode:
    """Root node for income. It countains income nodes (left side of the sankey diagram) and it contains issue nodes (right side of the sankey diagram)."""

    def __init__(self, label):
        """Initialize the income node."""
        self.label: str = label
        self.incomeNodes: list[SankeyNode] = []
        self.issueNodes: list[SankeyNode] = []

    def add_issue(self, issieNode: SankeyNode):
        """Add an issue to the income node."""
        self.issueNodes.append(issieNode)

    def add_income(self, incomeNode: SankeyNode):
        """Add an income to the income node."""
        self.incomeNodes.append(incomeNode)

    def get_issues_amount(self):
        """Get the total amount of issues."""
        return sum([child.amount for child in self.issueNodes])

    def get_income_amount(self):
        """Get the total amount of income."""
        return sum([parent.amount for parent in self.incomeNodes])
