from .events import CourseEventType


class EventBuilder:
    def __init__(self, events: list[CourseEventType]):
        self._events = events

    def insert(self, index: int, event: CourseEventType) -> None:
        self._events.insert(index, event)

    def replace(self, index: int, event: CourseEventType) -> None:
        self._events[index] = event

    def remove(self, index: int) -> None:
        self._events.pop(index)

    def append(self, event: CourseEventType) -> None:
        self._events.append(event)

    def build(self) -> list[CourseEventType]:
        return list(self._events)
