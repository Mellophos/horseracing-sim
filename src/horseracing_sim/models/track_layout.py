from typing import Literal

from .events import CourseEventType


class TrackLayout:
    def __init__(
            self,
            *,
            layout: Literal["loop", "linear"],
            width: float,
            events: list[CourseEventType],
            lap_distance: int | None = None
    ):
        self.layout = layout
        self.width = width
        self.events = sorted(events, key=lambda e: e.trigger_at)
        if self.layout == "loop":
            if not lap_distance:
                raise ValueError(
                    "lap_distance must be specified for loop layout")
            self.lap_distance = lap_distance
        else:
            if lap_distance:
                raise ValueError("lap_distance not needed for linear layout")

    def _build_events_for_loop(self, distance: int) -> list[CourseEventType]:
        event_list = []
        total_dist = distance
        laps = total_dist // self.lap_distance + 1
        for lap in range(laps):
            for idx, event in enumerate(self.events[1:-1]):
                if event.trigger_at > distance:
                    break

                event_list.append(
                    event.model_copy(
                        update={"trigger_at": distance - event.trigger_at}
                    )
                )

            distance -= self.lap_distance

        event_list.append(
            self.events[0].model_copy(
                update={"trigger_at": total_dist}
            )
        )

        return sorted(event_list, key=lambda e: (e.trigger_at, e.id))

    def _build_events_for_linear(self, distance: int) -> list[CourseEventType]:
        event_list = []
        for event in self.events[1:]:
            if event.trigger_at > distance:
                break

            event_list.append(
                event.model_copy(
                    update={"trigger_at": distance - event.trigger_at}
                )
            )

        event_list.append(
            self.events[0].model_copy(
                update={"trigger_at": distance}
            )
        )

        return sorted(event_list, key=lambda e: (e.trigger_at, e.id))

    def events_until(self, distance: int) -> list[CourseEventType]:
        if self.layout == "loop":
            return self._build_events_for_loop(distance)
        elif self.layout == "linear":
            return self._build_events_for_linear(distance)
        raise ValueError(f"Unknown layout: {self.layout!r}")
