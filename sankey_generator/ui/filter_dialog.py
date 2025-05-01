from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from sankey_generator.models.key_value_item import KeyValueItem

from sankey_generator.ui.ui_observable_base_window import UiObservableBaseWindow


class KeyValueItemDialog(QDialog, UiObservableBaseWindow):
    """Dialog for adding or editing a key value item."""

    def __init__(
        self, parent, window_title: str, key_string: str, value_string: str, current_item: KeyValueItem = None
    ):
        super().__init__(parent)
        self.key_value_item = current_item
        self.key_string = key_string
        self.value_string = value_string
        self.setWindowTitle(window_title)
        self.setMinimumSize(300, 200)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText(self.key_string)
        if self.key_value_item:
            self.key_input.setText(self.key_value_item.key)
        form_layout.addRow(self.key_string, self.key_input)

        self.values_input = QLineEdit(self)
        self.values_input.setPlaceholderText(self.value_string)
        if self.key_value_item:
            self.values_input.setText(', '.join(self.key_value_item.value))
        form_layout.addRow(self.value_string, self.values_input)

        layout.addLayout(form_layout)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_item)
        layout.addWidget(save_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def save_item(self):
        """Save the item."""
        key_value = self.key_input.text().strip()
        values = self.values_input.text().strip().split(',')

        if not key_value or not values:
            QMessageBox.warning(self, 'Invalid Input', 'Both fields are required.')
            return

        self.key_value_item = KeyValueItem(key_value, [value.strip() for value in values])
        self.accept()

    def get_item(self) -> KeyValueItem:
        """Return the created or edited item."""
        return self.key_value_item
