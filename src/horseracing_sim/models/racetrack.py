from collections.abc import Callable
from typing import ClassVar, Iterable

from .course import Course
from .event_builder import EventBuilder
from .events import CourseEventType
from .track_layout import TrackLayout
from ..constants import Surface

DistLayoutConfig = dict[tuple[int, str], TrackLayout]
Configuration = dict[Surface, DistLayoutConfig]


class Racetrack:
    NAME: ClassVar[str]
    DIST_CONFIGS: ClassVar[Configuration] = {}

    def get_track(
            self,
            surface: Surface,
            distance: int,
            layout: str
    ) -> tuple[TrackLayout, str]:
        surface_config = self.DIST_CONFIGS.get(surface)
        if surface_config is None:
            available_surfaces = ", ".join(
                s.name.lower() for s in self.DIST_CONFIGS
            )
            raise KeyError(
                f"No tracks configured for {surface.name!r}. "
                f"Available surfaces: {available_surfaces}"
            )

        track = surface_config.get((distance, layout))

        if track is not None:
            return track, layout

        available_layouts = [
            name
            for dist, name in surface_config
            if dist == distance
        ]

        if available_layouts:
            raise KeyError(
                f"No tracks configured for: "
                f"{surface.name!r}, {distance!r}, {layout!r}. "
                f"Available layouts for this distance: {available_layouts!r}"
            )

        available_distances = sorted({
            dist for dist, _ in surface_config
        })

        raise KeyError(
            f"No tracks configured for: "
            f"{surface.name!r}, {distance!r}, {layout}. "
            f"Available distances: {available_distances}."
        )

    def _get_builder(
            self,
            surface: Surface,
            distance: int,
            layout: str,
    ) -> Callable[[EventBuilder], list[CourseEventType]] | None:
        surface_name = surface.name.lower()

        candidates = [
            f"build_{surface_name}_{distance}_{layout}",
            f"build_{surface_name}_{distance}"
        ]

        for name in candidates:
            builder: Callable[[EventBuilder], list[CourseEventType]] | None = (
                getattr(self, name, None)
            )
            if builder is not None:
                if not callable(builder):
                    raise TypeError(f"{name!r} must be callable.")
                return builder
        return None

    def get_course(
            self,
            surface: Surface,
            distance: int,
            layout: str = "main"
    ) -> Course:
        track, layout = self.get_track(surface, distance, layout)
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

    def __init_subclass__(cls) -> None:
        if "NAME" not in cls.__dict__:
            raise AttributeError(f"{cls.__name__} has no NAME attribute.")
        if "DIST_CONFIGS" not in cls.__dict__:
            raise AttributeError(
                f"{cls.__name__} has no DIST_CONFIGS attribute.")
        super().__init_subclass__()


def track_config(
        track: TrackLayout,
        distances: Iterable[int],
        layout: str = "main"
) -> DistLayoutConfig:
    configs = {}
    for dist in distances:
        configs[(dist, layout)] = track
    return configs
