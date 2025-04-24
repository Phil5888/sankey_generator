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

    def add_issues(self, issueNodes: list[SankeyNode]):
        """Add issues to the income node."""
        self.issueNodes += issueNodes

    def add_income(self, incomeNode: SankeyNode):
        """Add an income to the income node."""
        self.incomeNodes.append(incomeNode)

    def add_incomes(self, incomeNodes: list[SankeyNode]):
        """Add incomes to the income node."""
        self.incomeNodes += incomeNodes

    def get_issues_amount(self):
        """Get the total amount of issues."""
        return sum([child.amount for child in self.issueNodes])

    def get_income_amount(self):
        """Get the total amount of income."""
        return sum([parent.amount for parent in self.incomeNodes])
