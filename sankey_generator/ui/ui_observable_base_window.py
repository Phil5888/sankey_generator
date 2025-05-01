"""Base class for the UI windows. Provides an interface for the controller to update the UI."""

from PyQt6.QtWidgets import QMessageBox
from sankey_generator.utils.observer import Observer, ObserverKeys


class UiObservableBaseWindow(Observer):
    """Base class for the UI windows."""

    def __init__(self):
        """Initialize the base window."""
        super().__init__()
        self.controller = None

    def update(self, observable, *args, **kwargs):
        """Update method for the observer pattern."""
        if self.controller is None:
            raise ValueError('Controller is not set. Please set the controller before calling update.')
        if observable == self.controller:
            if args[0] == ObserverKeys.INFO_MESSAGE and isinstance(args[1], str):
                # Show an info message
                QMessageBox.information(self, 'Info', args[1])
            elif args[0] == ObserverKeys.ERROR_MESSAGE and isinstance(args[1], str):
                # Show an error message
                QMessageBox.critical(self, 'Error', args[1])
