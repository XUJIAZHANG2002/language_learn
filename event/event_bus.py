"""
EventBus: a singleton publish-subscribe system for decoupled communication
between components (e.g., detector, heatmap, speaker).
"""


class EventBus:
    _instance = None
# singleton pattern
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def subscribe(self, event_type, callback):
        """Subscribe callback to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        """Remove callback from subscriber list."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def publish(self, event_type, data=None):
        """Trigger event with optional data payload."""
        if event_type not in self._subscribers:
            return
        for callback in self._subscribers[event_type]:
            callback(data)
