# Test stand-in for ableton.v3.control_surface.component.
class Component:
    def __init__(self, name = None, *a, song = None, **k):
        self.name = name
        self.song = song
