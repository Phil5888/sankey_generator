"""Implementation for observer pattern."""


class ObserverKeys:
    """Keys for the observer pattern."""

    THEME_CHANGED = 'theme'
    SANKEY_GENERATED = 'sankey_generated'
    OBSERVER_KEYS_MAIN_WINDOW = {THEME_CHANGED, SANKEY_GENERATED}

    INFO_MESSAGE = 'info_message'
    ERROR_MESSAGE = 'error_message'
    OBSERVER_KEYS_MESSAGE_BOX = {INFO_MESSAGE, ERROR_MESSAGE}

    CLOSE_WINDOW = 'close_window'
    OBSERVER_KEAYS_WINDOW = {CLOSE_WINDOW}


class Observable:
    """Observable class to be used as a base class for any observable object."""

    def __init__(self):
        """Initialize the observable with an empty list of observers."""
        self.observers: list[Observer] = []

    def add_observer(self, observer):
        """Add an observer to the list of observers."""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer from the list of observers."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        """Notify all observers about an event."""
        if (
            args[0] not in ObserverKeys.OBSERVER_KEYS_MAIN_WINDOW
            and args[0] not in ObserverKeys.OBSERVER_KEYS_MESSAGE_BOX
            and args[0] not in ObserverKeys.OBSERVER_KEAYS_WINDOW
        ):
            raise ValueError(f'Unknown observable: {args[0]}')
        for observer in self.observers:
            observer.updateObservable(self, *args, **kwargs)


class Observer:
    """Observer class to be used as a base class for any observer object."""

    def updateObservable(self, observable, *args, **kwargs):
        """Update method to be implemented by concrete observers."""
        pass
