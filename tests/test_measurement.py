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


@pytest.fixture
def unit_4_si():
    return Unit(name="test", in_si=4)

@pytest.fixture
def dist_2_ft():
    return Distance(2, unit=DistanceUnit.FT)

@pytest.fixture
def weight_2_pood():
    return Weight(2, unit=WeightUnit.POOD)


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


@pytest.mark.parametrize(
    "text",
    [
        "100 lb 2",
        "10 kg m"
    ]
)
def test_get_value_and_unit_raises(text):
    with pytest.raises(ValueError):
        _, _ = get_value_and_unit(text)


def test_get_value_and_unit_unknown_unit():
    with pytest.raises(UnknownUnitError):
        _, _ = get_value_and_unit("200 NotAUnit")


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

    def test_from_str(self):
        dist = Distance.from_str("2 mile")
        assert isinstance(dist, Distance)
        assert dist.si_unit == DistanceUnit.M
        assert dist.value == 2
        assert isinstance(dist.unit, Unit)
        assert dist.unit.name == DistanceUnit.MILE


    def test_str_(self, dist_2_ft):
        assert str(dist_2_ft) == "2 ft"

    def test_repr_(self, dist_2_ft):
        assert repr(dist_2_ft) == "0.6096 m"
    
    def test_si_value(self, dist_2_ft):
        assert dist_2_ft.si_value == 0.6096


class TestWeight:
    def test_init(self):
        weight = Weight(1.8, unit="kg")
        assert weight.value == 1.8
        assert isinstance(weight.unit, Unit)

    def test_from_str(self):
        dist = Weight.from_str("3.5 lb")
        assert isinstance(dist, Weight)
        assert dist.si_unit == WeightUnit.KG
        assert dist.value == 3.5
        assert isinstance(dist.unit, Unit)
        assert dist.unit.name == WeightUnit.LB

    def test_init_raises(self):
        with pytest.raises(UnknownUnitError):
            _ = Weight(42, unit="wrong")

    def test_str_(self, weight_2_pood):
        assert str(weight_2_pood) == "2 pood"

    def test_repr_(self, weight_2_pood):
        assert repr(weight_2_pood) == "32 kg"
    
    def test_si_value(self, weight_2_pood):
        assert weight_2_pood.si_value == 32