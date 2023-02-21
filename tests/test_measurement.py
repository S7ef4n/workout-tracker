import pytest

from workout_tracker.measurement import (
    Distance,
    Unit,
    DistanceUnit,
    WeightUnit,
    UnknownUnitError,
    Weight,
    get_value_and_unit,
)


@pytest.mark.parametrize(
    "text, exp_value, exp_str",
    [
        ("150lb", 150, "lb"),
        ("2 pood", 2, "pood"),
        ("mile 1.6", 1.6, "mile"),
        ("ft3.2", 3.2, "ft"),
    ],
)
def test_get_value_and_unit(text, exp_value, exp_str):
    value, unit = get_value_and_unit(string=text)
    assert value == exp_value
    assert unit == exp_str
    assert (unit in DistanceUnit) or (unit in WeightUnit)


@pytest.fixture
def unit_4_si():
    return Unit(name="test", in_si=4)


class TestUnit:
    def test_init(self):
        unit = Unit(name="kg", in_si=1)
        assert isinstance(unit, Unit)

    def test_from_si(self, unit_4_si):
        assert unit_4_si.to_si(1) == 4
        assert unit_4_si.to_si(1.3) == 5.2

    def test_to_si(self, unit_4_si):
        assert unit_4_si.from_si(1) == 0.25
        assert unit_4_si.from_si(4.4) == 1.1


class TestDistance:
    def test_init(self):
        dist = Distance(1.3, unit="m")
        assert dist.value == 1.3
        assert isinstance(dist.unit, Unit)

    def test_init_raises(self):
        with pytest.raises(UnknownUnitError):
            _ = Distance(1.3, unit="wrong")


class TestWeight:
    def test_init(self):
        weight = Weight(1.8, unit="kg")
        assert weight.value == 1.8
        assert isinstance(weight.unit, Unit)

    def test_init_raises(self):
        with pytest.raises(UnknownUnitError):
            _ = Weight(42, unit="wrong")
