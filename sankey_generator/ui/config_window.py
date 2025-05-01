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


class ConfigWindow(QDialog):
    """Configuration window for editing config values."""

    def __init__(self, config_service):
        """Initialize the configuration window."""
        super().__init__()
        self.config_service = config_service
        self.config = config_service.config
        self.setWindowTitle('Configuration')
        self.setMinimumSize(500, 400)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel('Configuration', self))

        # Tab Widget
        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

        # Add tabs
        self.init_issues_tab()
        self.init_income_filters_tab()
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

    def init_issues_tab(self):
        """Initialize the Issues Data Frame Filters tab."""
        self.issues_tab = QWidget()
        tab_layout = QVBoxLayout()

        self.issues_filter_list = QListWidget(self)
        self.load_issues_filters()
        tab_layout.addWidget(self.issues_filter_list)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Add Filter', self)
        add_button.clicked.connect(self.add_issues_filter)
        button_layout.addWidget(add_button)

        edit_button = QPushButton('Edit Filter', self)
        edit_button.clicked.connect(self.edit_issues_filter)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Delete Filter', self)
        delete_button.clicked.connect(self.delete_issues_filter)
        button_layout.addWidget(delete_button)

        tab_layout.addLayout(button_layout)
        self.issues_tab.setLayout(tab_layout)
        self.tab_widget.addTab(self.issues_tab, 'Issues Filters')

    def init_income_filters_tab(self):
        """Initialize the Income Data Frame Filters tab."""
        self.income_filters_tab = QWidget()
        tab_layout = QVBoxLayout()

        self.income_filter_list = QListWidget(self)
        self.load_income_filters()
        tab_layout.addWidget(self.income_filter_list)

        button_layout = QHBoxLayout()

        add_button = QPushButton('Add Filter', self)
        add_button.clicked.connect(self.add_income_filter)
        button_layout.addWidget(add_button)

        edit_button = QPushButton('Edit Filter', self)
        edit_button.clicked.connect(self.edit_income_filter)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Delete Filter', self)
        delete_button.clicked.connect(self.delete_income_filter)
        button_layout.addWidget(delete_button)

        tab_layout.addLayout(button_layout)
        self.income_filters_tab.setLayout(tab_layout)
        self.tab_widget.addTab(self.income_filters_tab, 'Income Filters')

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

        delete_button = QPushButton('Delete Account', self)
        delete_button.clicked.connect(self.delete_income_account)
        button_layout.addWidget(delete_button)

        tab_layout.addLayout(button_layout)
        self.income_accounts_tab.setLayout(tab_layout)
        self.tab_widget.addTab(self.income_accounts_tab, 'Income Accounts')

    def load_issues_filters(self):
        """Load issues filters into the list widget."""
        self.issues_filter_list.clear()
        for filter_item in self.config.issues_data_frame_filters:
            self.issues_filter_list.addItem(
                f'{filter_item.csv_column_name}: {", ".join(filter_item.csv_value_filters)}'
            )

    def load_income_filters(self):
        """Load income filters into the list widget."""
        self.income_filter_list.clear()
        for filter_item in self.config.income_data_frame_filters:
            self.income_filter_list.addItem(
                f'{filter_item.csv_column_name}: {", ".join(filter_item.csv_value_filters)}'
            )

    def load_income_accounts(self):
        """Load income reference accounts into the list widget."""
        self.income_accounts_list.clear()
        for account in self.config.income_reference_accounts:
            self.income_accounts_list.addItem(f'{account.account_name} ({account.iban})')

    def add_issues_filter(self):
        """Add a new issues filter."""
        dialog = FilterDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_filter = dialog.get_filter()
            self.config.issues_data_frame_filters.append(new_filter)
            self.load_issues_filters()

    def edit_issues_filter(self):
        """Edit the selected issues filter."""
        selected_item = self.issues_filter_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to edit.')
            return

        current_filter = self.config.issues_data_frame_filters[selected_item]
        dialog = FilterDialog(self, current_filter)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_filter = dialog.get_filter()
            self.config.issues_data_frame_filters[selected_item] = updated_filter
            self.load_issues_filters()

    def delete_issues_filter(self):
        """Delete the selected issues filter."""
        selected_item = self.issues_filter_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to delete.')
            return

        del self.config.issues_data_frame_filters[selected_item]
        self.load_issues_filters()

    def add_income_filter(self):
        """Add a new income filter."""
        dialog = FilterDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_filter = dialog.get_filter()
            self.config.income_data_frame_filters.append(new_filter)
            self.load_income_filters()

    def edit_income_filter(self):
        """Edit the selected income filter."""
        selected_item = self.income_filter_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to edit.')
            return

        current_filter = self.config.income_data_frame_filters[selected_item]
        dialog = FilterDialog(self, current_filter)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_filter = dialog.get_filter()
            self.config.income_data_frame_filters[selected_item] = updated_filter
            self.load_income_filters()

    def delete_income_filter(self):
        """Delete the selected income filter."""
        selected_item = self.income_filter_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to delete.')
            return

        del self.config.income_data_frame_filters[selected_item]
        self.load_income_filters()

    def add_income_account(self):
        """Add a new income reference account."""
        account_name, iban = self.get_account_details()
        if account_name and iban:
            self.config.income_reference_accounts.append(AccountSource(account_name, iban))
            self.load_income_accounts()

    def delete_income_account(self):
        """Delete the selected income reference account."""
        selected_item = self.income_accounts_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select an account to delete.')
            return

        del self.config.income_reference_accounts[selected_item]
        self.load_income_accounts()

    def save_changes(self):
        """Save changes to the config."""
        # TBD: Validate the config before saving

        self.config_service._save_config()
        QMessageBox.information(self, 'Saved', 'Configuration saved successfully.')
        self.close()
