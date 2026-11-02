from .events import CourseEventType


class EventBuilder:
    def __init__(self, events: list[CourseEventType]):
        self._events = events

    def insert(self, index: int, event: CourseEventType) -> None:
        self._events.insert(index, event)

    def replace(self, index: int, event: CourseEventType) -> None:
        self._events[index] = event

    def modify(self, index: int, **kwargs) -> None:
        if "id" in kwargs:
            raise ValueError("id cannot be modified")

        self._events[index] = self._events[index].model_copy(update=kwargs)

    def remove(self, *indexes: int) -> None:
        for index in sorted(indexes, reverse=True):
            self._events.pop(index)

    def append(self, event: CourseEventType) -> None:
        self._events.append(event)

    def build(self) -> list[CourseEventType]:
        return list(self._events)
