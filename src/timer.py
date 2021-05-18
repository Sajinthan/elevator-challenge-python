import threading
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


class SetInterval(Generic[T]):
    def __init__(self, func: T, sec: int) -> None:
        def callback():
            self.t = threading.Timer(sec, callback)
            self.t.start()
            func()

        self.t = threading.Timer(sec, callback)
        self.t.start()

    def cancel(self) -> None:
        self.t.cancel()
