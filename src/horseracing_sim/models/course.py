from typing import Self, Any

from pydantic import BaseModel, ConfigDict, Field, model_validator, \
    field_validator

from .events import CourseEventType
from ..constants import Surface, DistanceCat


class Course(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    version: str = Field(alias="$version")
    id: str = Field(
        pattern=r"^course_[0-9]{5}_(?:turf|dirt|artificial)_[a-z]+_[0-9]{4}$"
    )

    name: str = Field(min_length=1)
    surface: Surface
    distance: int = Field(ge=1000, le=5000)
    width: float = Field(ge=1)
    events: list[CourseEventType] = Field(default_factory=list)

    def __init__(
            self,
            /,
            *,
            layout: str = "main",
            **data: Any):
        if "version" not in data and "$version" not in data:
            data["version"] = "course-0.1.0"

        if "id" not in data:
            surface = data.get("surface")
            distance = data.get("distance")

            if surface is not None and distance is not None:
                surface_name = (
                    surface.name.lower()
                    if isinstance(surface, Surface)
                    else str(surface).lower()
                )

                data["id"] = (
                    f"course_90000_{surface_name}_{layout.lower()}_{distance}"
                )
        super().__init__(**data)

    @property
    def distance_cat(self) -> DistanceCat:
        return DistanceCat.from_distance(self.distance)

    @property
    def layout(self) -> str:
        return self.id.split("_")[3]

    @model_validator(mode="after")
    def validate_id_consistency(self) -> Self:
        _, _, id_surface, _, id_distance = self.id.split("_")

        if id_surface.upper() != self.surface.name:
            raise ValueError(
                f"ID surface '{id_surface}' does not match "
                f"surface attribute '{self.surface.name}'"
            )

        if int(id_distance) != self.distance:
            raise ValueError(
                f"ID distance '{id_distance}' does not match "
                f"distance attribute '{self.distance}'"
            )

        return self

    @field_validator("events", mode="after")
    @classmethod
    def sort_events(cls, events: list[CourseEventType]) -> list[
        CourseEventType]:
        return sorted(events, key=lambda e: (e.trigger_at, e.id))
