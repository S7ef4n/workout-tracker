from abc import ABC
from dataclasses import dataclass
from datetime import timedelta

from workout_tracker.exercise import Exercise


@dataclass
class Workout(ABC):
    """Parent class for all workout types"""


@dataclass
class Amrap(Workout):
    """
    Class for AMRAP style workouts.
    """

    duration: timedelta
    exercises: list[Exercise]
    buy_in: Workout | None = None
    repeats: int = 1
    rest: timedelta | None = None
    buy_out: Workout | None = None
