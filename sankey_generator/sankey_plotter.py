"""SankeyPlotter class."""

import plotly.graph_objects as go
import random
import plotly.io as pio

from sankey_generator.models.sankey_income_node import SankeyIncomeNode
from sankey_generator.models.sankey_node import SankeyNode


class SankeyPlotter:
    """SankeyPlotter class."""

    def __init__(self, amount_out_name: str):
        """Initialize the SankeyPlotter."""
        self.amount_out_name = amount_out_name

    def add_nodes_to_sankey(
        self,
        node: SankeyNode,
        labels: list[str],
        source: list[int],
        target: list[int],
        values: list[float],
        colors: list[int],
        parent_index=None,
    ):
        """Add nodes to the sankey diagram."""
        if node.label not in labels:
            labels.append(node.label)
        node_index = labels.index(node.label)

        if parent_index is not None:
            source.append(parent_index)
            target.append(node_index)
            values.append(node.amount)
            colors.append('#%06x' % random.randint(0, 0xFFFFFF))

        for issueNode in node.childNodes:
            self.add_nodes_to_sankey(issueNode, labels, source, target, values, colors, node_index)

    def add_income_node_to_sankey(
        self,
        income_node: SankeyIncomeNode,
        labels: list[str],
        source: list[int],
        target: list[int],
        values: list[float],
        colors: list[int],
        parent_index=None,
    ):
        """Add income nodes to the sankey diagram."""
        for current_income in income_node.incomeNodes:
            labels.append(current_income.label)
            source.append(labels.index(current_income.label))
            values.append(current_income.amount)
            # add random color
            colors.append('#%06x' % random.randint(0, 0xFFFFFF))

        labels.append(income_node.label)
        income_node_index = len(labels) - 1
        target += [income_node_index] * len(income_node.incomeNodes)

        if income_node.label not in labels:
            labels.append(income_node.label)
        node_index = labels.index(income_node.label)

        if parent_index is not None:
            source.append(parent_index)
            target.append(node_index)
            values.append(income_node.amount)
            colors.append('#%06x' % random.randint(0, 0xFFFFFF))

        for issueNode in income_node.issueNodes:
            self.add_nodes_to_sankey(issueNode, labels, source, target, values, colors, node_index)

    def get_sankey_html(self, income_node: SankeyIncomeNode, year: int, month: int) -> str:
        """Plot the sankey diagram and return it as an HTML div."""
        fig = self.get_sankey_fig(income_node, year, month)
        return pio.to_html(fig, full_html=False)

    def get_sankey_fig(self, income_node: SankeyIncomeNode, year: int, month: int) -> go.Figure:
        """Get the sankey diagram Figure."""
        labels: list[str] = []
        source: list[int] = []
        values: list[float] = []
        colors: list[int] = []
        target: list[int] = []

        self.add_income_node_to_sankey(income_node, labels, source, target, values, colors)

        fig = go.Figure(
            data=[
                go.Sankey(
                    valueformat='.00f',
                    valuesuffix='€',
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color='black', width=0.5),
                        label=labels,
                        color=colors,
                        hovertemplate=f'{self.amount_out_name} %{{value}}<extra></extra>',
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=values,
                        hovercolor=colors,
                        hovertemplate=f'{self.amount_out_name}: %{{value}}<extra></extra>',
                    ),
                )
            ]
        )

        fig.update_layout(
            hovermode='x',
            title=dict(text=f'Finanzguru Sankey Diagramm {year}-{month:02d}', font=dict(size=20, color='white')),
            font=dict(size=10, color='white'),
            plot_bgcolor='black',
            paper_bgcolor='black',
        )

        return fig
