from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from sankey_generator.models.config import DataFrameFilter

from sankey_generator.ui.ui_observable_base_window import UiObservableBaseWindow


class FilterDialog(QDialog, UiObservableBaseWindow):
    """Dialog for adding or editing a filter."""

    def __init__(self, parent, filter_item=None):
        super().__init__(parent)
        self.filter_item = filter_item
        self.setWindowTitle('Add/Edit Filter')
        self.setMinimumSize(300, 200)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.column_name_input = QLineEdit(self)
        self.column_name_input.setPlaceholderText('Column Name')
        if self.filter_item:
            self.column_name_input.setText(self.filter_item.csv_column_name)
        form_layout.addRow('Column Name:', self.column_name_input)

        self.values_input = QLineEdit(self)
        self.values_input.setPlaceholderText('Comma-separated values')
        if self.filter_item:
            self.values_input.setText(', '.join(self.filter_item.csv_value_filters))
        form_layout.addRow('Values:', self.values_input)

        layout.addLayout(form_layout)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_filter)
        layout.addWidget(save_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def save_filter(self):
        """Save the filter."""
        column_name = self.column_name_input.text().strip()
        values = self.values_input.text().strip().split(',')

        if not column_name or not values:
            QMessageBox.warning(self, 'Invalid Input', 'Both fields are required.')
            return

        self.filter_item = DataFrameFilter(column_name, [value.strip() for value in values])
        self.accept()

    def get_filter(self):
        """Return the created or edited filter."""
        return self.filter_item
