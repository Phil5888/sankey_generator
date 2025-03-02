"""NiceGUI will run the sankey generator."""

import os
from nicegui import ui
from sankey_generator.models.csv_filter import CsvFilter
from sankey_generator.models.data_frame_filter import DataFrameFilter
from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.theme import Theme
from sankey_generator.models.config import Config
import os.path
import platform

# TODO List:
# - Add a way to select the input file
# - Add a way to select the output file
# - Add a way to select the reference accounts
# - Add a way to select the income sources
# - Add a way to select the income node name
# - Add a way to select the not used income names
# - Add a way to select the analysis year column name
# - Add a way to select the analysis month column name
# - Add a way to select the amount out name
# - Add a way to select the other income name
# - Add a way to select the issue level
# - Add a way to select the income data frame filters
# - Add a way to select the issues data frame filters
# - Add a way to select the income reference accounts
# - Add a way to select the issues reference accounts
# - Add a config file to save the settings
# - Add budget indecator to sankey diagram
# - Split income to reference accounts (Requires ignoring "Umbuchung" in the CSV)
# - Add subcategories for fix costs and variable costs
# - Create a diagramm only for fix costs and variable costs

# Load configuration
config = Config('config.json')

# Create required folders
os.makedirs('input_files', exist_ok=True)
os.makedirs('output_files', exist_ok=True)

# Configure parser and plotter
fcp = FinanzguruCsvParser(
    config.column_analysis_main_category,
    config.column_analysis_sub_category,
    config.analysis_year_column_name,
    config.analysis_month_column_name,
    config.income_node_name,
    config.amount_out_name,
    config.other_income_name,
    config.not_used_income_names,
)
sp = SankeyPlotter(config.amount_out_name)

income_sources = [CsvFilter(src['label'], src['column'], src['values']) for src in config.income_sources]

income_data_frame_filters = [DataFrameFilter(flt['column'], flt['values']) for flt in config.income_data_frame_filters]

issues_data_frame_filters = [DataFrameFilter(flt['column'], flt['values']) for flt in config.issues_data_frame_filters]


def generate_sankey(year, month, issue_level):
    """Generate the Sankey diagram for the given year, month and issue level."""
    # Parse CSV and plot Sankey diagram
    income_node = fcp.parse_csv(
        config.input_file,
        income_sources,
        year,
        month,
        issue_level,
        income_data_frame_filters,
        issues_data_frame_filters,
    )

    # Generate the interactive Sankey diagram as an HTML div
    fig = sp.get_sankey_fig(income_node, year, month)

    # Separate the HTML and JavaScript content
    # fig = sankey_html.replace('<div>', '').replace('</div>', '').replace('<script>', '').replace('</script>', '')

    print('Sankey generated')

    return fig


theme = Theme()

ui.colors(
    primary=theme.primary,
    secondary=theme.secondary,
    accent=theme.accent,
    dark=theme.dark,
    dark_page=theme.dark_page,
    positive=theme.positive,
    negative=theme.negative,
    info=theme.info,
    warning=theme.warning,
)
# TODO: Set colors in sankey

dark = ui.dark_mode()
ui.label('Switch mode:')
ui.button('Dark', on_click=dark.enable)
ui.button('Light', on_click=dark.disable)

with ui.dialog() as dialog, ui.card():
    result = ui.markdown()

with ui.row().classes('items-center'):
    year = ui.input('Year', value='2024')
    month = ui.input('Month', value='1')
    issue_level = ui.input('Issue level', value='1')

    def on_submit(year: int, month: int, issue_level: int):
        """Generate the Sankey diagram for the given year, month and issue level."""
        print(f'Generating Sankey diagram for {year}-{month} with issue level {issue_level}')

        fig = generate_sankey(year, month, issue_level)

        diagram = ui.plotly(fig).classes('w-full h-2000')
        diagram_container.clear()
        diagram.move(diagram_container)
        # ui_label.move(diagram_container)

    ui.button(
        'Start Sankey generation',
        on_click=lambda: on_submit(int(year.value), int(month.value), int(issue_level.value)),
    ).props('no-caps')

with ui.row().classes('items-center'):
    ui.label('Sankey diagram:')

with ui.row().classes('items-center'):
    diagram_container = ui.html().classes('mt-4')

# NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
ui.run(reload=platform.system() != 'Windows')
