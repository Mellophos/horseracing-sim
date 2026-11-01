from pprint import pprint

from .constants import Surface
from .models.course import Course
from .models.event_builder import EventBuilder
from .models.horse import Horse
from . import assets
from .models.events import Straight, Slope, Corner
from .models.racetrack import Racetrack
from .models.track_layout import TrackLayout
from .validation.json_validator import validate_json


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

    CONFIGS = {
        Surface.TURF: Racetrack.track_config(
            turf_main,
            {1400, 1600, 1800, 2000, 2300, 2400, 2500, 2600, 3400},
        )
    }

    @staticmethod
    def build_turf_1400(events: EventBuilder):
        events.insert(
            0,
            Straight(
                trigger_at=0,
                type=2,
                straight_id=2,
                is_start=True,
            )
        )


def main():
    tokyo = Tokyo()
    course = tokyo.get_course(Surface.TURF, 1400)
    print(course.id)
    pprint(course.events[0])



def horse_model():
    horse_json = assets.horse.get("horse_00001")
    horse = Horse.model_validate(horse_json)
    pprint(horse)

    pprint(assets.horse.list_all())


def course_model():
    course_json = {
        "$version": "course-0.1.0",
        "id": "course_10006_turf_main_1400",
        "name": "Tokyo",
        "surface": 0,
        "distance": 1400,
        "width": 30,
        "events": [
            {
                "id": 0,
                "trigger_at": 0,
                "is_start": True,
                "straight_id": 0,
                "type": 1
            },
            {
                "id": 0,
                "trigger_at": 1400,
                "is_start": False,
                "straight_id": 0,
                "type": 1
            },
        ]
    }

    validate_json(course_json)
    course = Course.model_validate(course_json)
    print(course)

    course_json = course.model_dump_json(indent=4)
    print(course_json)
