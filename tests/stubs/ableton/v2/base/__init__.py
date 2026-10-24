# ==================================================
#
# This file is part of CustomMaschineMK3.
# CustomMaschineMK3 is free software licensed under GPL-3.0.
# For more details, see "LICENSE" file.
#
# Copyright (C) 2026 Caparrini
#
# ==================================================

# Minimal stand-ins for the parts of ableton.v2.base used by the banking code.
class _Listener:
    def __init__(self): self.subject = None
    def replace_subjects(self, subjects): self.subjects = list(subjects)
class _ListenDescriptor:
    def __init__(self, fn): self.fn = fn; self.name = '_listener_' + fn.__name__
    def __get__(self, obj, owner):
        if obj is None: return self
        if self.name not in obj.__dict__: obj.__dict__[self.name] = _Listener()
        return obj.__dict__[self.name]
def listens(*a, **k): return lambda fn: _ListenDescriptor(fn)
listens_group = listens
def listenable_property(fn): return property(fn)
class EventObject:
    def __init__(self, *a, **k): pass
    def register_disconnectable(self, d): return d
    def unregister_disconnectable(self, d): pass
def clamp(v, lo, hi): return max(lo, min(v, hi))
def find_if(pred, seq):
    for x in seq:
        if pred(x): return x
    return None
def liveobj_valid(obj): return obj is not None
def old_hasattr(obj, name): return hasattr(obj, name)
def _notify_any(self, *a, **k): pass
EventObject.__getattr__ = lambda self, name: (lambda *a, **k: None) if name.startswith('notify_') else (_ for _ in ()).throw(AttributeError(name))
