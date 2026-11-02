from .event_builder import EventBuilder
from .events import Straight, Slope, Corner
from .racetrack import Racetrack, track_config
from .track_layout import TrackLayout
from ..constants import Surface


class Tokyo(Racetrack):
    NAME = "Tokyo"
    turf_main = TrackLayout(
        layout="loop",
        lap_distance=2083,
        width=30,
        events=[
            Straight(trigger_at=0, type=1, straight_id=1, is_start=False),
            Slope(trigger_at=471, gradient=1.19, length=176),
            Straight(trigger_at=525, type=1, straight_id=1, is_start=True),
            Corner(trigger_at=770, number=4, length=245, direction=-1),
            Slope(trigger_at=882, gradient=0.1, length=411),
            Corner(trigger_at=1035, number=3, length=265, direction=-1),
            Straight(trigger_at=1035, type=2, straight_id=2, is_start=False),
            Slope(trigger_at=1145, gradient=-0.84, length=263),
            Slope(trigger_at=1281, gradient=1.75, length=80),
            Straight(trigger_at=1479, type=2, straight_id=2, is_start=True),
            Corner(trigger_at=1737, number=2, length=258, direction=-1),
            Slope(trigger_at=1898, gradient=-0.28, length=617),
            Corner(trigger_at=2000, number=1, length=263, direction=-1),
            Straight(trigger_at=2000, type=1, straight_id=1, is_start=False),
            Straight(trigger_at=2083, type=1, straight_id=1, is_start=True)
        ]
    )
    niigata_straight = TrackLayout(
        layout="linear",
        width=25,
        events=[
            Straight(trigger_at=0, type=1, straight_id=1, is_start=False),
            Slope(trigger_at=460, gradient=-0.71, length=134),
            Slope(trigger_at=561, gradient=0.6, length=101),
            Slope(trigger_at=760, gradient=-1.0, length=199),
            Slope(trigger_at=1000, gradient=0.8, length=240),
            Straight(trigger_at=1000, type=1, straight_id=1, is_start=True)
        ]
    )

    DIST_CONFIGS = {
        Surface.TURF: {
            **track_config(
                turf_main,
                {1400, 1600, 1800, 2000, 2300, 2400, 2500, 2600, 3400}
            ),
            **track_config(
                niigata_straight,
                {1000, 1600},
                "straight"
            )
        }
    }

    @staticmethod
    def build_turf_1400_main(events: EventBuilder):
        events.insert(
            0,
            Slope(trigger_at=0, gradient=-0.28, length=119)
        )
        events.insert(
            0,
            Straight(
                trigger_at=0, type=2, straight_id=2, is_start=True)
        )

    @staticmethod
    def build_turf_1600_main(events: EventBuilder):
        events.modify(
            0,
            trigger_at=0
        )

    @staticmethod
    def build_turf_1800_main(events: EventBuilder):
        events.modify(
            0,
            trigger_at=160, length=171
        )

    @staticmethod
    def build_turf_2000_main(events: EventBuilder):
        events.remove(0, 1)
        events.modify(
            0,
            trigger_at=387, length=332
        )
        events.modify(
            1,
            trigger_at=155, length=275
        )
        events.modify(
            2,
            trigger_at=430
        )

    @staticmethod
    def build_turf_2300_main(events: EventBuilder):
        events.insert(
            0,
            Straight(trigger_at=0, type=1, straight_id=1, is_start=True)
        )

    @staticmethod
    def build_turf_2400_main(events: EventBuilder):
        events.insert(
            0,
            Straight(trigger_at=0, type=1, straight_id=1, is_start=True)
        )
        events.insert(
            0,
            Slope(trigger_at=0, gradient=1.19, length=22)
        )

    @staticmethod
    def build_turf_2500_main(events: EventBuilder):
        events.insert(
            0,
            Straight(trigger_at=0, type=1, straight_id=1, is_start=True)
        )
        events.insert(
            0,
            Slope(trigger_at=0, gradient=1.19, length=122)
        )

    @staticmethod
    def build_turf_3400_main(events: EventBuilder):
        events.insert(
            0,
            Straight(trigger_at=0, type=2, straight_id=2, is_start=True)
        )
        events.insert(
            0,
            Slope(trigger_at=0, gradient=-0.28, length=36)
        )
