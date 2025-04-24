"""Finanzguru CSV parser."""

import pandas as pd
from sankey_generator.models.sankey_node import SankeyNode
from sankey_generator.models.sankey_income_node import SankeyRootNode
from sankey_generator.models.config import DataFrameFilter, AccountSource, IssueCategory


class FinanzguruCsvParser:
    """Finanzguru CSV parser."""

    def __init__(
        self,
        issues_hierarchy: IssueCategory,
        analysis_year_column_name: str,
        analysis_month_column_name: str,
        income_node_name: str,
        amount_out_name: str,
        other_income_name: str,
        not_used_income_names: list[str],
    ):
        """Initialize the Finanzguru CSV parser."""
        self.issues_hierarchy = issues_hierarchy
        self.analysis_year_column_name = analysis_year_column_name
        self.analysis_month_column_name = analysis_month_column_name
        self.income_node_name = income_node_name
        self.amount_out_name = amount_out_name
        self.other_income_name = other_income_name
        self.not_used_income_names = not_used_income_names

    def _get_sum(self, df: pd.DataFrame) -> float:
        """Return the sum of column in the DataFrame."""
        df = df.str.replace('.', '').str.replace(',', '.').astype(float)
        sum = df.sum()
        if sum < 0:
            sum = sum * -1
        return sum

    def _get_sum_for_value_in_column(self, df: pd.DataFrame, column: str, values_filter: list[str]) -> float:
        """Return the sum of the column in the DataFrame where the 'column' contains 'value_lowercase'."""
        sum = 0
        for value in values_filter:
            filtered_df = df.loc[(df[column].str.lower().str.contains(value.lower())), self.amount_out_name]
            sum = sum + self._get_sum(filtered_df)
        return sum

    def _get_relevant_data_from_csv(
        self,
        file_path: str,
        year: int,
        month: int,
    ) -> pd.DataFrame:
        """Get relevant data from the Finanzguru CSV file."""
        df = pd.read_csv(file_path, sep=';', decimal=',')

        # fill all empty cells in each column with "empty"
        df = df.fillna('empty')

        if month is None:
            df = df.loc[(df[self.analysis_year_column_name] == year)]
        else:
            df = df.loc[(df[self.analysis_month_column_name] == f'{year}-{month:02d}')]

        return df

    def _create_income_nodes(self, income_df: pd.DataFrame, income_accounts: list[AccountSource]) -> list[SankeyNode]:
        """Create income nodes from the income DataFrame and income sources."""
        income_nodes: list[SankeyNode] = []
        for income_source in income_accounts:
            for income_filter in income_source.income_filters:
                sum = self._get_sum_for_value_in_column(
                    income_df, income_filter.csv_column_name, income_filter.csv_value_filters
                )
                income_nodes.append(SankeyNode(sum, income_filter.sankey_label))

        # add other income to income_nodes
        sum_other_income = self._get_sum(income_df[self.amount_out_name])
        for node in income_nodes:
            sum_other_income -= node.amount

        income_nodes.append(SankeyNode(sum_other_income, self.other_income_name))
        return income_nodes

    def _create_issue_nodes(
        self,
        issues_df: pd.DataFrame,
        issue_category: IssueCategory,
        used_category_names: list[str],
        issue_depth: int,
    ) -> list[SankeyNode]:
        """Create issue nodes from the issues DataFrame and main categories."""
        issue_nodes: list[SankeyNode] = []
        if issue_category is None:
            return issue_nodes
        if issue_depth < 1:
            return issue_nodes

        issues_current_category = issues_df[issue_category.csv_column_name].unique()
        for category in issues_current_category:
            sum = self._get_sum_for_value_in_column(issues_df, issue_category.csv_column_name, [category])

            if category in used_category_names:
                # add a invisible space to the category name to avoid circular reference
                category = f' {category}'

            current_category_node = SankeyNode(sum, category)

            category_df = issues_df.loc[
                issues_df[issue_category.csv_column_name].str.lower().str.contains(category.lower())
            ]

            used_category_names.append(category)
            sub_nodes = self._create_issue_nodes(
                category_df, issue_category.sub_category, used_category_names, issue_depth - 1
            )
            for sub_node in sub_nodes:
                current_category_node.add_linked_node(sub_node)

            issue_nodes.append(current_category_node)
        return issue_nodes

    def configure_parser(
        self,
        file_path: str,
        income_sources: list[AccountSource],
        income_data_frame_fitlers: list[DataFrameFilter],
        issues_data_frame_fitlers: list[DataFrameFilter],
    ) -> None:
        """Configure the parser."""
        self.file_path = file_path
        self.income_sources = income_sources
        self.income_data_frame_fitlers = income_data_frame_fitlers
        self.issues_data_frame_fitlers = issues_data_frame_fitlers

    def parse_csv(
        self,
        year: int,
        month: int,
        issue_depth: int,
    ) -> SankeyRootNode:
        """Parse the Finanzguru CSV file and return a DataFrame."""
        if issue_depth < 1:
            raise ValueError('issue_level must be greater than 0')
        max_issue_level = self.issues_hierarchy.get_depth()
        if issue_depth > max_issue_level:
            raise ValueError(f'issue_level must be less than or equal to {max_issue_level}')
        if month is not None:
            if self.analysis_month_column_name is None:
                raise ValueError('analysis_month_column_name must be set if month is not None')

        df: pd.DataFrame = self._get_relevant_data_from_csv(
            self.file_path,
            year,
            month,
        )

        income_df: pd.DataFrame = df
        for data_frame_filter in self.income_data_frame_fitlers:
            income_df = income_df.loc[df[data_frame_filter.csv_column_name].isin(data_frame_filter.csv_value_filters)]

        issues_df: pd.DataFrame = df
        for data_frame_filter in self.issues_data_frame_fitlers:
            issues_df = issues_df.loc[df[data_frame_filter.csv_column_name].isin(data_frame_filter.csv_value_filters)]

        root_node = SankeyRootNode(self.income_node_name)

        income_nodes = self._create_income_nodes(income_df, self.income_sources)
        for income_node_item in income_nodes:
            root_node.add_income(income_node_item)

        # We need to know all used category names because sankey plot will add a circular reference if node name is ussed multiple times
        used_category_names: list[str] = []
        issue_nodes = self._create_issue_nodes(issues_df, self.issues_hierarchy, used_category_names, issue_depth)
        for issue_node in issue_nodes:
            root_node.add_issue(issue_node)

        # not used income
        unused_income = root_node.get_income_amount() - root_node.get_issues_amount()
        if unused_income > 0:
            unused_income_node = SankeyNode(unused_income, self.not_used_income_names[0])

            if issue_depth == 2:
                unused_income_node.add_linked_node(SankeyNode(unused_income, self.not_used_income_names[1]))

            root_node.add_issue(unused_income_node)

        return root_node
