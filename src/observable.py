from typing import Any, Callable, Dict, List
from enums import Event

Observer = Dict[Event, List[Callable[[Any], None]]]
Subscription = Dict[str, Callable]


class Observable:
    observers: Observer

    def __init__(self) -> None:
        self.observers = {}

    def subscribe(self, event_enum: Event, fn: Callable[[Any], None]) -> Subscription:
        event = str(event_enum)
        if isinstance(fn, Callable):
            if hasattr(self.observers, event):
                self.observers[event].append(fn)
            else:
                self.observers[event] = [fn]

            return {"unsubscribe": self.unsubscribe_func(event, fn)}

        else:
            print("Not a function")

    def unsubscribe_func(self, event: str, callback: Callable[[Any], None]) -> None:
        def unsubscribe() -> None:
            filtered_list = list(
                filter(lambda x: (x != callback), self.observers.get(event))
            )
            self.observers[event] = filtered_list

        return unsubscribe

    def publish(self, event_enum: Event, params: Any) -> None:
        event = str(event_enum)
        callbacks = self.observers.get(event)

        for callback in callbacks:
            callback(params)
