import threading
import functools

def singleton(originCls):
    originNew = originCls.__new__
    originInit = originCls.__init__
    instance = None
    _lock: threading.Lock = threading.Lock()

    @functools.wraps(originCls.__new__)
    def __new__(cls,*args, **kwargs):
        nonlocal instance
        nonlocal _lock

        with _lock:
            if instance is None:
                instance = originNew(cls, *args, **kwargs)
                instance.__setattr__("__initialized__", False)

        return instance
    
    @functools.wraps(originCls.__init__)
    def __init__(cls,*args, **kwargs):
        nonlocal instance
        nonlocal _lock

        with _lock:
            if not instance.__initialized__:
                instance.__initialized__ = True
                originInit(cls, *args, **kwargs)

    
    originCls.__new__ = __new__
    originCls.__init__ = __init__

    return originCls