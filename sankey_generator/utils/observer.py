"""Implementation for observer pattern."""


class ObserverKeys:
    """Keys for the observer pattern."""

    THEME_CHANGED = 'theme'
    SANKEY_GENERATED = 'sankey_generated'
    OBSERVER_KEYS_MAIN_WINDOW = {THEME_CHANGED, SANKEY_GENERATED}


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
        if args[0] not in ObserverKeys.OBSERVER_KEYS_MAIN_WINDOW:
            raise ValueError(f'Unknown observable: {args[0]}')
        for observer in self.observers:
            observer.update(self, *args, **kwargs)


class Observer:
    """Observer class to be used as a base class for any observer object."""

    def update(self, observable, *args, **kwargs):
        """Update method to be implemented by concrete observers."""
        pass
