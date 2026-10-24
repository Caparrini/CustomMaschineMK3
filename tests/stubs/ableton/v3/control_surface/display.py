# Test stand-in for ableton.v3.control_surface.display: records notifications.
class Renderable:
    notifications = None
    def notify(self, notification, *a):
        self.__dict__.setdefault("notified", []).append(notification(*a) if callable(notification) else notification)
