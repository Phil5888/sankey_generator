"""Configuration window for editing config values."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
)
from sankey_generator.ui.filter_dialog import FilterDialog


class ConfigWindow(QDialog):
    """Configuration window for editing issues_data_frame_filters."""

    def __init__(self, config_service):
        """Initialize the configuration window."""
        super().__init__()
        self.config_service = config_service
        self.config = config_service.config
        self.setWindowTitle('Configuration')
        self.setMinimumSize(400, 300)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel('Edit Issues Data Frame Filters', self))

        # List of filters
        self.filter_list = QListWidget(self)
        self.load_filters()
        layout.addWidget(self.filter_list)

        # Buttons for adding, editing, and deleting filters
        button_layout = QHBoxLayout()

        add_button = QPushButton('Add Filter', self)
        add_button.clicked.connect(self.add_filter)
        button_layout.addWidget(add_button)

        edit_button = QPushButton('Edit Filter', self)
        edit_button.clicked.connect(self.edit_filter)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton('Delete Filter', self)
        delete_button.clicked.connect(self.delete_filter)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        # Save and Cancel buttons
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def load_filters(self):
        """Load filters into the list widget."""
        self.filter_list.clear()
        for filter_item in self.config.issues_data_frame_filters:
            self.filter_list.addItem(f'{filter_item.csv_column_name}: {", ".join(filter_item.csv_value_filters)}')

    def add_filter(self):
        """Add a new filter."""
        dialog = FilterDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_filter = dialog.get_filter()
            self.config.issues_data_frame_filters.append(new_filter)
            self.load_filters()

    def edit_filter(self):
        """Edit the selected filter."""
        selected_item = self.filter_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to edit.')
            return

        current_filter = self.config.issues_data_frame_filters[selected_item]
        dialog = FilterDialog(self, current_filter)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_filter = dialog.get_filter()
            self.config.issues_data_frame_filters[selected_item] = updated_filter
            self.load_filters()

    def delete_filter(self):
        """Delete the selected filter."""
        selected_item = self.filter_list.currentRow()
        if selected_item < 0:
            QMessageBox.warning(self, 'No Selection', 'Please select a filter to delete.')
            return

        del self.config.issues_data_frame_filters[selected_item]
        self.load_filters()

    def save_changes(self):
        """Save changes to the config."""
        self.config_service.save_config()
        QMessageBox.information(self, 'Saved', 'Configuration saved successfully.')
        self.close()
