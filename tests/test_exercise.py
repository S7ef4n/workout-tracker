from datetime import timedelta

import pytest
from hypothesis import given, settings
from hypothesis.strategies import (
    builds,
    floats,
    from_regex,
    integers,
    sampled_from,
    timedeltas,
)

from workout_tracker.exercise import Exercise, to_str
from workout_tracker.measurement import (
    Distance,
    DistanceUnit,
    Weight,
    WeightUnit,
)


def test_to_str():
    assert to_str(None) == ""
    assert to_str("some string") == "some string"
    assert to_str(23) == "23"


class TestExercise:
    def test_init(self):
        exercise = Exercise(
            name="back squat", reps=5, weight=Weight(value=100, unit="kg")
        )
        assert exercise.name == "Back Squat"

    def test_init_raises(self):
        with pytest.raises(ValueError):
            _ = Exercise(
                name="back squat",
                height=Distance(value=10, unit=DistanceUnit.CM),
                weight=Weight(value=100, unit="kg"),
            )

    def test_init_recursive(self):
        exercise = Exercise(
            name="Clean & Jerk",
            reps=5,
            weight=Weight(value=50, unit="lb"),
            sub_exercises=[
                Exercise(name="Clean", reps=3),
                Exercise(name="Jerk", reps=1),
            ],
        )
        assert exercise.name == "3 Clean + 1 Jerk"

    def test_init_recursive_raises(self):
        with pytest.raises(ValueError):
            _ = Exercise(
                name=None,
                reps=3,
                weight=Weight(value=50, unit="lb"),
                sub_exercises=[
                    Exercise(
                        name="Snatch",
                        reps=3,
                        weight=Weight(value=10, unit="kg"),
                    ),
                    Exercise(
                        name="Box Jump",
                        reps=1,
                        height=Distance(value=24, unit="in"),
                    ),
                ],
            )

    def test_from_dict(self):
        ex_dict = {"name": "Box Jump", "reps": 20, "height": "24 in"}
        exercise = Exercise.from_dict(exercise_dict=ex_dict)
        assert exercise.name == "Box Jump"
        assert exercise.reps == 20
        assert exercise.height == Distance(value=24, unit=DistanceUnit.INCH)

        ex_dict = {"name": "Handstand Hold", "duration": "01:30"}
        exercise = Exercise.from_dict(exercise_dict=ex_dict)
        assert exercise.name == "Handstand Hold"
        assert exercise.duration == timedelta(seconds=90)

    @pytest.mark.parametrize(
        "exercise",
        [
            Exercise(
                name="Box Jump", reps=5, height=Distance(24, DistanceUnit.INCH)
            ),
            Exercise(name="Clean", reps=5, weight=Weight(100, WeightUnit.KG)),
            Exercise(
                name="Row", reps=5, distance=Distance(500, DistanceUnit.M)
            ),
            Exercise(name="Handstand Hold", duration=timedelta(seconds=30)),
        ],
    )
    def test_to_dict(self, exercise):
        out_dict = exercise.to_dict()
        assert None not in out_dict.values()

    def test_to_dict_multiple(self):
        exercise = Exercise(
            name=None,
            reps=5,
            weight=Weight(value=50, unit="lb"),
            sub_exercises=[
                Exercise(name="Clean", reps=3),
                Exercise(name="Jerk", reps=1),
            ],
        )
        out_dict = exercise.to_dict()
        assert set(out_dict.keys()) == {
            "name",
            "reps",
            "weight",
            "sub_exercises",
        }
        assert out_dict["name"] == "3 Clean + 1 Jerk"
        assert out_dict["reps"] == 5
        assert out_dict["weight"] == "50 lb"
        clean_dict = {"name": "Clean", "reps": 3}
        jerk_dict = {"name": "Jerk", "reps": 1}
        assert clean_dict in out_dict["sub_exercises"]
        assert jerk_dict in out_dict["sub_exercises"]
        assert len(out_dict["sub_exercises"]) == 2

    def test_to_and_from_dict_multiple(self):
        exercise = Exercise(
            name=None,
            reps=5,
            weight=Weight(value=50, unit="lb"),
            sub_exercises=[
                Exercise(name="Clean", reps=3),
                Exercise(name="Jerk", reps=1),
            ],
        )
        out_dict = exercise.to_dict()
        re_read_exercise = Exercise.from_dict(exercise_dict=out_dict)
        assert exercise == re_read_exercise

    @given(
        string=from_regex(r"([A-Za-z]+\s+)+"),
        reps=integers(min_value=1, max_value=1_000),
        duration=timedeltas(
            min_value=timedelta(seconds=1), max_value=timedelta(hours=2)
        ),
        weight=builds(
            Weight,
            value=floats(min_value=0.1, max_value=100),
            unit=sampled_from(WeightUnit),
        ),
        distance=builds(
            Distance,
            value=floats(min_value=0.1, max_value=1_000),
            unit=sampled_from(DistanceUnit),
        ),
        height=builds(
            Distance,
            value=floats(min_value=0.1, max_value=10),
            unit=sampled_from(DistanceUnit),
        ),
    )
    @settings(max_examples=50)
    def test_to_and_from_dict(
        self, string, reps, duration, weight, distance, height
    ):
        exercise = Exercise(
            name=string,
            reps=reps,
            weight=weight,
            duration=duration,
            distance=distance,
            height=height,
        )
        out_dict = exercise.to_dict()
        re_read_exercise = Exercise.from_dict(exercise_dict=out_dict)
        assert exercise == re_read_exercise

    @pytest.mark.parametrize(
        "exercise, string",
        [
            (
                Exercise(
                    name="Box Jump",
                    reps=5,
                    height=Distance(24, DistanceUnit.INCH),
                ),
                "5 Box Jump 24 in",
            ),
            (
                Exercise(
                    name="Back Squat",
                    reps=5,
                    weight=Weight(100, WeightUnit.KG),
                ),
                "5 Back Squat 100 kg",
            ),
            (
                Exercise(
                    name="Run", reps=5, distance=Distance(500, DistanceUnit.M)
                ),
                "5 500 m Run",
            ),
            (
                Exercise(
                    name="Handstand Hold", duration=timedelta(seconds=30)
                ),
                "0:00:30 Handstand Hold",
            ),
        ],
    )
    def test_str(self, exercise, string):
        assert str(exercise) == string
