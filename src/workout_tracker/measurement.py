from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

from workout_tracker.better_enum import BetterStrEnum


def get_value_and_unit(
    string: str,
) -> tuple[float, DistanceUnit | WeightUnit]:
    """
    Extracts the value and unit from a string.
    Expects only one number and one word in the given input string.

    Args:
        string (str): String from which to extract value and unit.

    Raises:
        ValueError: If more than one number in string.
        ValueError: If more than one word in string.
        UnknownUnitError: If unit is unknown.

    Returns:
        tuple[float, DistanceUnit | WeightUnit]: Value and unit
    """
    if len(values := re.findall(r"\d+\.?\d*", string)) != 1:
        raise ValueError("Input text needs to contain exactly one number!")
    if len(units := re.findall(r"[^\d\W]+", string)) != 1:
        raise ValueError("Input text needs to contain exactly one unit!")

    unit = units[0]
    if (unit not in DistanceUnit) and (unit not in WeightUnit):
        raise UnknownUnitError(f"The input unit of {unit} is unknown.")

    return float(values[0]), unit


class UnknownUnitError(Exception):
    """Error raised when unit is unknown."""


UNIT_CONVERSIONS = {
    "km": 1000,
    "m": 1,
    "cm": 0.01,
    "mile": 1609.344,
    "yard": 0.9144,
    "ft": 0.3048,
    "in": 0.0254,
    "kg": 1,
    "lb": 0.45359237,
    "pood": 16,
}


class DistanceUnit(BetterStrEnum):
    """
    Class to store all valid distance units
    """

    KM = "km"
    M = "m"
    CM = "cm"
    MILE = "mile"
    YARD = "yard"
    FT = "ft"
    INCH = "in"


class WeightUnit(BetterStrEnum):
    """
    Class to store all valid weight units
    """

    KG = "kg"
    LB = "lb"
    POOD = "pood"


@dataclass
class Unit:
    """
    Handles a measurement unit
    """

    name: str
    in_si: float

    def from_si(self, value: float) -> float:
        """
        Translates value to SI units

        Args:
            value (float): Value in given unit.

        Returns:
            float: Value in SI units.
        """
        return value / self.in_si

    def to_si(self, value: float) -> float:
        """
        Translates value from SI units

        Args:
            value (float): Value in SI units.

        Returns:
            float: Value in given unit.
        """
        return value * self.in_si


class Measurement(ABC):
    """
    Class to handle distance measurement together with its unit.
    """

    @abstractmethod
    def __init__(self, value: float, unit: DistanceUnit | WeightUnit) -> None:
        self.value = value
        self.si_unit = "Undefined"
        self.unit = Unit(name=str(unit), in_si=UNIT_CONVERSIONS[unit])

    def __str__(self) -> str:
        """
        Represents measurement as string in given unit

        Returns:
            str: Measurement and unit
        """
        return str(self.value) + " " + self.unit.name

    def __eq__(self, other: object) -> bool:
        """
        Check equality between instances. Returns True if object is of the
        same class and represents the same value in SI units.

        Args:
            other (object): Object to compare self to.

        Returns:
            bool: Whether measurements are equal.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        same_value = self.si_value == other.si_value
        same_si = self.si_unit == other.si_unit
        return same_si and same_value

    @property
    def si_value(self) -> float:
        """
        Get value of measurement in SI units.

        Returns:
            float: Measurement value in SI units.
        """
        return self.unit.to_si(self.value)

    @classmethod
    def from_str(cls, string: str) -> Self:
        """
        Generates an instance of the values given in a string.

        Args:
            string (str): String consisting of a number and a word denoting
                the value and unit of the measurement.

        Returns:
            Self: Initialized self class
        """
        value, unit_str = get_value_and_unit(string=string)
        return cls(value=value, unit=unit_str)


class Distance(Measurement):
    """
    Class to handle distance measurement together with its unit.
    """

    def __init__(self, value: float, unit: DistanceUnit) -> None:
        """
        Class to handle distance measurement together with its unit.

        Args:
            value (float): Value of the distance measurement.
            unit (DistanceUnit): Unit of the distance.

        Raises:
            UnknownUnitError: If given distance unit is unknown.
        """
        if unit not in DistanceUnit:
            raise UnknownUnitError(f"The input unit of {unit} is unknown.")
        super().__init__(value=value, unit=unit)
        self.si_unit = DistanceUnit.M


class Weight(Measurement):
    """
    Class to handle weight measurement together with its unit.
    """

    def __init__(self, value: float, unit: WeightUnit) -> None:
        """
        Class to handle weight measurement together with its unit.

        Args:
            value (float): Value of the weight measurement.
            unit (WeightUnit): Unit of the weight.

        Raises:
            UnknownUnitError: Is raised if weight unit is not known.
        """
        if unit not in WeightUnit:
            raise UnknownUnitError(f"The input unit of {unit} is unknown.")
        super().__init__(value=value, unit=unit)
        self.si_unit = WeightUnit.KG
