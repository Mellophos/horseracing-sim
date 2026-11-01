from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar, Iterable

from .course import Course
from .event_builder import EventBuilder
from .events import CourseEventType
from .track_layout import TrackLayout
from ..constants import Surface

DistLayoutConfig = dict[tuple[int, str], TrackLayout]
Configuration = dict[Surface, DistLayoutConfig]


@dataclass(frozen=True)
class CourseConfig:
    surface: Surface
    distance: int
    layout: str


class Racetrack:
    NAME: ClassVar[str]
    CONFIGS: ClassVar[Configuration] = {}

    def get_track(
            self,
            surface: Surface,
            distance: int,
            layout: str = "main"
    ) -> TrackLayout:
        try:
            return self.CONFIGS[surface][(distance, layout)]
        except KeyError:
            raise AttributeError(
                f"No track found for: {surface!r}, {distance!r}, {layout!r}"
            )

    def _get_builder(
            self,
            surface: Surface,
            distance: int,
            layout: str,
    ) -> Callable[list[CourseEventType], list[CourseEventType]] | None:
        surface_name = surface.name.lower()

        candidates = [
            f"build_{surface_name}_{distance}_{layout}",
            f"build_{surface_name}_{distance}"
        ]

        for name in candidates:
            builder = getattr(self, name, None)
            if builder is not None:
                if not callable(builder):
                    raise TypeError(f"{name!r} is not callable.")
                return builder
        return None

    def get_course(
            self,
            surface: Surface,
            distance: int,
            layout: str = "main"
    ) -> Course:
        track = self.get_track(surface, distance, layout)
        event_builder = EventBuilder(
            track.events_until(distance)
        )
        builder = self._get_builder(surface, distance, layout)

        if builder is not None:
            builder(event_builder)

        event_list = event_builder.build()

        return Course(
            name=self.NAME,
            surface=surface,
            distance=distance,
            layout=layout,
            width=track.width,
            events=event_list,
        )

    @staticmethod
    def track_config(
            track: TrackLayout,
            distances: Iterable[int],
            layout: str = "main"
    ) -> DistLayoutConfig:
        configs = {}
        for dist in distances:
            configs[(dist, layout)] = track
        return configs
