# Test stand-ins for ableton.v3.control_surface.controls: event decorators return the
# function unchanged, so tests call the handlers directly.
class _Control:
    def __init__(self, *a, **k): pass
    def _decorator(self, fn): return fn
    pressed = released = value = double_clicked = _decorator
class ButtonControl(_Control): pass
class InputControl(_Control): pass
