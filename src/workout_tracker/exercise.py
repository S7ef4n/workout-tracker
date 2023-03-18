from __future__ import annotations

import string
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Self

import pytimeparse

from workout_tracker.measurement import Distance, Weight


def to_str(obj: Any) -> str:
    """
    Converts object to string by calling the str() method or if None/False
    return empty string.

    Args:
        obj (Any): Object to convert.

    Returns:
        str: Resulting string.
    """
    return str(obj or "")


@dataclass
class Exercise:
    """
    Dataclass to store exercises
    """

    name: str
    reps: int | None = None
    weight: Weight | None = None
    duration: timedelta | None = None
    distance: Distance | None = None
    height: Distance | None = None
    sub_exercises: list[Exercise] | None = None

    def __post_init__(self) -> None:
        """
        Checks that one of the arguments reps, duration or distance is set.

        Raises:
            ValueError: Is raised if reps, duration and
                distance attributes are all None.
        """
        if not any([self.reps, self.duration, self.distance]):
            raise ValueError("Reps, duration or distance needs to be set.")

        if self.sub_exercises is not None:
            self.name = " + ".join([str(ex) for ex in self.sub_exercises])
            cond = (
                any(ex.weight for ex in self.sub_exercises)
                | any(ex.distance for ex in self.sub_exercises)
                | any(ex.height for ex in self.sub_exercises)
                | any(ex.duration for ex in self.sub_exercises)
                | any(ex.sub_exercises for ex in self.sub_exercises)
            )
            if cond:
                raise ValueError(
                    "Weight, distance, height and duration can "
                    + "only be set for the entire complex."
                )
        else:
            self.name = string.capwords(self.name.strip())

    @classmethod
    def from_dict(cls, exercise_dict: dict) -> Self:
        """
        Initializes an exercise instance from a given dictionary.

        Args:
            exercise_dict (dict): Dictionary describing the exercise.

        Returns:
            Self: Initialized Exercise instance.
        """
        default_exercise_dict = defaultdict(lambda: None, exercise_dict)
        if default_exercise_dict["weight"] is not None:
            default_exercise_dict["weight"] = Weight.from_str(
                default_exercise_dict["weight"]
            )
        if default_exercise_dict["duration"] is not None:
            default_exercise_dict["duration"] = timedelta(
                seconds=pytimeparse.parse(default_exercise_dict["duration"])
            )
        if default_exercise_dict["distance"] is not None:
            default_exercise_dict["distance"] = Distance.from_str(
                default_exercise_dict["distance"]
            )
        if default_exercise_dict["height"] is not None:
            default_exercise_dict["height"] = Distance.from_str(
                default_exercise_dict["height"]
            )
        if default_exercise_dict["sub_exercises"] is not None:
            default_exercise_dict["sub_exercises"] = [
                cls.from_dict(d)
                for d in default_exercise_dict["sub_exercises"]
            ]

        return cls(
            name=exercise_dict["name"],
            reps=default_exercise_dict["reps"],
            weight=default_exercise_dict["weight"],
            duration=default_exercise_dict["duration"],
            distance=default_exercise_dict["distance"],
            height=default_exercise_dict["height"],
            sub_exercises=default_exercise_dict["sub_exercises"],
        )

    def to_dict(self) -> dict:
        """
        Parse exercise description to a dictionary.

        Returns:
            dict: Dictionary containing the exercise description.
        """
        sub_dicts = None
        if self.sub_exercises is not None:
            sub_dicts = [
                sub_exercise.to_dict() for sub_exercise in self.sub_exercises
            ]

        return_dict = {
            "name": self.name,
            "reps": self.reps,
            "weight": to_str(self.weight),
            "duration": to_str(self.duration),
            "distance": to_str(self.distance),
            "height": to_str(self.height),
            "sub_exercises": sub_dicts,
        }
        return {key: value for key, value in return_dict.items() if value}

    def __str__(self) -> str:
        """
        Represents exercise as string.

        Returns:
            str: Exercise as string.
        """

        return " ".join(
            filter(
                None,
                [
                    to_str(self.duration),
                    to_str(self.reps),
                    to_str(self.distance),
                    self.name,
                    to_str(self.weight),
                    to_str(self.height),
                ],
            )
        )
