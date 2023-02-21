from dataclasses import dataclass
from datetime import timedelta

from workout_tracker.measurement import Distance, Weight


@dataclass
class Exercise:
    """
    Dataclass to store exercises
    """

    name: str
    reps: int
    weight: Weight
    duration: timedelta
    distance: Distance
    height: Distance
