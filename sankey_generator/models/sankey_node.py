"""Model for a Sankey node."""


class SankeyNode:
    """
    Base Model for a Sankey node. A node can be a income or an issue.

    Linked nodes are:
    - Issue nodes (right side of the sankey diagram) and their sub categories.
    - Income nodes (left side of the sankey diagram) and their sub categories.
    """

    def __init__(self, amount: float, label: str):
        """Initialize the Sankey node."""
        self.amount = amount
        self.label = label
        self.linkedNodes: list[SankeyNode] = []

    def add_linked_node(self, child: 'SankeyNode'):
        """Add a child to the Sankey node."""
        self.linkedNodes.append(child)
