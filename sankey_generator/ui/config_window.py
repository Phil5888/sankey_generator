"""Configuration window for editing config values."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
    QTabWidget,
    QWidget,
)
from sankey_generator.ui.filter_dialog import FilterDialog
from sankey_generator.ui.ui_observable_base_window import UiObservableBaseWindow
from sankey_generator.models.config import AccountSource, DataFrameFilter
from sankey_generator.controllers.config_controller import ConfigController
from sankey_generator.utils.observer import ObserverKeys


class ConfigWindow(QDialog, UiObservableBaseWindow):
    """Configuration window for editing config values."""

    def __init__(self, controller: ConfigController):
        """Initialize the configuration window."""
        super().__init__()
        self.controller: ConfigController = controller
        self.setWindowTitle('Configuration')
        self.setMinimumSize(500, 400)
        self.init_ui()

    def updateObservable(self, observable, *args, **kwargs):
        """Update method for the observer pattern."""
        super().updateObservable(observable, *args, **kwargs)

        if observable == self.controller:
            if args[0] == ObserverKeys.CLOSE_WINDOW:
                self.close()
            elif args[0] == ObserverKeys.ISSUES_FITLERS_CHANGED:
                self.load_filters(self.issues_filter_list_widget, self.controller.issues_data_frame_filters)
            elif args[0] == ObserverKeys.INCOME_FITLERS_CHANGED:
                self.load_filters(self.income_filter_list_widget, self.controller.income_data_frame_filters)

        else:
            raise ValueError(f'Unknown observable: {observable}')

    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel('Configuration', self))

        # Tab Widget
        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

        # Add tabs
        self.issues_filter_list_widget = QListWidget(self)
        self.issues_filter_tab = self.init_filter_tab(
            self.issues_filter_list_widget,
            'issues filter',
            self.add_issues_filter,
            self.edit_issues_filter,
            self.delete_issues_filter,
        )
        self.load_filters(
            self.issues_filter_list_widget,
            self.controller.issues_data_frame_filters,
        )

        self.income_filter_list_widget = QListWidget(self)
        self.income_filter_tab = self.init_filter_tab(
            self.income_filter_list_widget,
            'income filters',
            self.add_income_filter,
            self.edit_income_filter,
            self.delete_income_filter,
        )
        self.load_filters(
            self.income_filter_list_widget,
            self.controller.income_data_frame_filters,
        )

        self.init_income_accounts_tab()

        # Save and Cancel buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def init_filter_tab(self, filter_list_widget: QListWidget, title: str, add_func, edit_func, delete_func) -> QWidget:
        """Initialize the Issues Data Frame Filters tab."""
        filter_tab = QWidget()
        tab_layout = QVBoxLayout()

        tab_layout.addWidget(filter_list_widget)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Add Filter', self)
        add_button.clicked.connect(add_func)
        button_layout.addWidget(add_button)

        edit_button = QPushButton('Edit Filter', self)
        edit_button.clicked.connect(edit_func)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Delete Filter', self)
        delete_button.clicked.connect(delete_func)
        button_layout.addWidget(delete_button)

        tab_layout.addLayout(button_layout)
        filter_tab.setLayout(tab_layout)
        self.tab_widget.addTab(filter_tab, title)
        return filter_tab

    def init_income_accounts_tab(self):
        """Initialize the Income Reference Accounts tab."""
        self.income_accounts_tab = QWidget()
        tab_layout = QVBoxLayout()

        self.income_accounts_list = QListWidget(self)
        self.load_income_accounts()
        tab_layout.addWidget(self.income_accounts_list)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Add Account', self)
        add_button.clicked.connect(self.add_income_account)
        button_layout.addWidget(add_button)

        edit_button = QPushButton('Edit Account', self)
        edit_button.clicked.connect(self.edit_income_account)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Delete Account', self)
        delete_button.clicked.connect(self.delete_income_account)
        button_layout.addWidget(delete_button)

        tab_layout.addLayout(button_layout)
        self.income_accounts_tab.setLayout(tab_layout)
        self.tab_widget.addTab(self.income_accounts_tab, 'Income Accounts')

    def load_filters(self, filter_list_widget: QListWidget, filters: list[DataFrameFilter]):
        """Load income filters into the list widget."""
        filter_list_widget.clear()
        filter: DataFrameFilter = None
        for filter in filters:
            filter_list_widget.addItem(f'{filter.csv_column_name}: {", ".join(filter.csv_value_filters)}')

    def load_income_accounts(self):
        """Load income reference accounts into the list widget."""
        self.income_accounts_list.clear()
        account: AccountSource = None
        for account in self.controller.income_reference_accounts:
            self.income_accounts_list.addItem(f'{account.account_name} ({account.iban})')

    def add_issues_filter(self):
        """Add a new issues filter."""
        self._add_filter('Add issues filter', 'Column name', 'Column value', self.controller.add_issues_filter)

    def add_income_filter(self):
        """Add a new income filter."""
        self._add_filter('Add income filter', 'Column name', 'Column value', self.controller.add_income_filter)

    def _add_filter(self, window_title: str, key_string: str, value_string: str, add_filter_func):
        """Add a new filter."""
        dialog = FilterDialog(self, window_title, key_string, value_string)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_filter = dialog.get_filter()
            add_filter_func(new_filter)

    def edit_issues_filter(self):
        """Edit the selected issues filter."""
        self._edit_filter(
            'Edit issues filter',
            'Column name',
            'Column value',
            self.controller.edit_issues_filter,
            self.issues_filter_list_widget,
            self.controller.issues_data_frame_filters,
        )

    def edit_income_filter(self):
        """Edit the selected income filter."""
        self._edit_filter(
            'Edit income filter',
            'Column name',
            'Column value',
            self.controller.edit_income_filter,
            self.income_filter_list_widget,
            self.controller.income_data_frame_filters,
        )

    def _edit_filter(
        self,
        window_title: str,
        key_string: str,
        value_string: str,
        update_func,
        filter_list_widget: QListWidget,
        filter_list: list[DataFrameFilter],
    ):
        """Edit the selected filter."""
        selected_item = filter_list_widget.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to edit.')
            return

        current_filter = filter_list[selected_item]
        dialog = FilterDialog(self, window_title, key_string, value_string, current_filter)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_filter = dialog.get_filter()
            update_func(selected_item, updated_filter)

    def delete_issues_filter(self):
        """Delete the selected issues filter."""
        self._delete_filter(self.controller.delete_issues_filter, self.issues_filter_list_widget)

    def delete_income_filter(self):
        """Delete the selected income filter."""
        self._delete_filter(self.controller.delete_income_filter, self.income_filter_list_widget)

    def _delete_filter(self, delete_func, filter_list_widget: QListWidget):
        """Delete the selected filter."""
        selected_item = filter_list_widget.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to delete.')
            return
        delete_func(selected_item)

    def add_income_account(self):
        """Add a new income reference account."""
        account_name, iban = self.get_account_details()
        if account_name and iban:
            self.controller.income_reference_accounts.append(AccountSource(account_name, iban))
            self.load_income_accounts()

    def edit_income_account(self):
        """Edit the selected income reference account."""
        selected_item = self.income_accounts_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select an account to edit.')
            return

        current_account = self.controller.income_reference_accounts[selected_item]
        account_name, iban = self.get_account_details(current_account)
        if account_name and iban:
            self.controller.income_reference_accounts[selected_item] = AccountSource(account_name, iban)
            self.load_income_accounts()

    def delete_income_account(self):
        """Delete the selected income reference account."""
        selected_item = self.income_accounts_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select an account to delete.')
            return

        self.controller.delete_income_reference_account(selected_item)

    def save_changes(self):
        """Save changes to the config."""
        # TBD: Validate the config before saving
        self.controller.save_config()
