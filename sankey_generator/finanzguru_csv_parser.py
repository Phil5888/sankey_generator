"""Finanzguru CSV parser."""

import pandas as pd
from sankey_generator.models.sankey_node import SankeyNode
from sankey_generator.models.sankey_income_node import SankeyIncomeNode
from sankey_generator.models.csv_filter import CsvFilter
from sankey_generator.models.issue_category import IssueCategory
from sankey_generator.models.data_frame_filter import DataFrameFilter


class FinanzguruCsvParser:
    """Finanzguru CSV parser."""

    def __init__(
        self,
        column_anaylsis_main_category: str,
        column_anaylsis_sub_category: str,
        analysis_year_column_name: str,
        analysis_month_column_name: str,
        income_node_name: str,
        amount_out_name: str,
        other_income_name: str,
        not_used_income_names: list[str],
    ):
        """Initialize the Finanzguru CSV parser."""
        self.column_anaylsis_main_category = column_anaylsis_main_category
        self.column_anaylsis_sub_category = column_anaylsis_sub_category
        self.analysis_year_column_name = analysis_year_column_name
        self.analysis_month_column_name = analysis_month_column_name
        self.income_node_name = income_node_name
        self.amount_out_name = amount_out_name
        self.other_income_name = other_income_name
        self.not_used_income_names = not_used_income_names

    def get_sum(self, df: pd.DataFrame) -> float:
        """Return the sum of column in the DataFrame."""
        df = df.str.replace('.', '').str.replace(',', '.').astype(float)
        sum = df.sum()
        if sum < 0:
            sum = sum * -1
        return sum

    def get_sum_for_value_in_column(self, df: pd.DataFrame, column: str, value_lowercase: str) -> float:
        """Return the sum of the column in the DataFrame where the 'column' contains 'value_lowercase'."""
        filtered_df = df.loc[(df[column].str.lower().str.contains(value_lowercase)), self.amount_out_name]
        return self.get_sum(filtered_df)

    def get_relevant_data_from_csv(
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

    def create_income_nodes(self, income_df: pd.DataFrame, income_sources: list[CsvFilter]) -> list[SankeyNode]:
        """Create income nodes from the income DataFrame and income sources."""
        income_nodes = []
        for income_source in income_sources:
            sum = self.get_sum_for_value_in_column(income_df, income_source.column_name, income_source.values[0])
            income_nodes.append(SankeyNode(sum, income_source.target_label, income_source))

        # add other income to income_nodes
        sum_other_income = self.get_sum(income_df[self.amount_out_name])
        for node in income_nodes:
            sum_other_income -= node.amount

        income_nodes.append(SankeyNode(sum_other_income, self.other_income_name, None))
        return income_nodes

    def create_issue_nodes(
        self,
        issues_df: pd.DataFrame,
        issues_main_categories: list[IssueCategory],
    ) -> list[SankeyNode]:
        """Create issue nodes from the issues DataFrame and main categories."""
        issue_nodes = []
        for main_category in issues_main_categories:
            csv_filter = CsvFilter(main_category.name, self.column_anaylsis_main_category, [main_category.name.lower()])

            sum = self.get_sum_for_value_in_column(issues_df, csv_filter.column_name, csv_filter.values[0])
            main_category_node = SankeyNode(sum, csv_filter.target_label, csv_filter)

            for sub_category in main_category.sub_categories:
                csv_filter = CsvFilter(sub_category, self.column_anaylsis_sub_category, [sub_category.lower()])

                sum = self.get_sum_for_value_in_column(issues_df, csv_filter.column_name, csv_filter.values[0])
                main_category_node.add_child(SankeyNode(sum, csv_filter.target_label, csv_filter))

            issue_nodes.append(main_category_node)
        return issue_nodes

    def parse_csv(
        self,
        file_path: str,
        income_sources: list[CsvFilter],
        year: int,
        month: int,
        issue_level: int,
        income_data_frame_fitlers: list[DataFrameFilter],
        issues_data_frame_fitlers: list[DataFrameFilter],
    ) -> SankeyIncomeNode:
        """Parse the Finanzguru CSV file and return a DataFrame."""
        if issue_level not in [1, 2]:
            raise ValueError('issue_level must be 1 or 2')
        if issue_level == 2:
            if self.column_anaylsis_sub_category is None:
                raise ValueError('column_anaylsis_sub_category must be set if issue_level is 2')
            if len(self.not_used_income_names) != 2:
                raise ValueError('not_used_income_names must have a length of 2 if issue_level is 2')
        if month is not None:
            if self.analysis_month_column_name is None:
                raise ValueError('analysis_month_column_name must be set if month is not None')

        df: pd.DataFrame = self.get_relevant_data_from_csv(
            file_path,
            year,
            month,
        )

        income_df: pd.DataFrame = df
        for data_frame_filter in income_data_frame_fitlers:
            income_df = income_df.loc[df[data_frame_filter.column].isin(data_frame_filter.values)]

        issues_df: pd.DataFrame = df
        for data_frame_filter in issues_data_frame_fitlers:
            issues_df = issues_df.loc[df[data_frame_filter.column].isin(data_frame_filter.values)]

        issues_main_categories_str: str = issues_df[self.column_anaylsis_main_category].unique()

        issues_main_categories: list[IssueCategory] = []
        for category in issues_main_categories_str:
            issue_sub_categories = []
            if issue_level == 2 and self.column_anaylsis_sub_category is not None:
                issue_sub_categories = issues_df.loc[
                    (issues_df[self.column_anaylsis_main_category] == category),
                    self.column_anaylsis_sub_category,
                ].unique()
            issues_main_categories.append(IssueCategory(category, issue_sub_categories))

        income_nodes = self.create_income_nodes(income_df, income_sources)
        income_node = SankeyIncomeNode(self.income_node_name, income_nodes)

        issue_nodes = self.create_issue_nodes(issues_df, issues_main_categories)
        for issue_node in issue_nodes:
            income_node.add_issue(issue_node)

        # not used income
        unused_income = income_node.get_income_amount() - income_node.get_issues_amount()
        if unused_income > 0:
            unused_income_node = SankeyNode(unused_income, self.not_used_income_names[0], None)

            if issue_level == 2:
                unused_income_node.add_child(SankeyNode(unused_income, self.not_used_income_names[1], None))

            income_node.add_issue(unused_income_node)

        return income_node
