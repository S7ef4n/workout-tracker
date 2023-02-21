from enum import EnumMeta, StrEnum
from typing import Any


class MetaEnum(EnumMeta):
    """
    MetaEnum class with contains method.
    """

    def __contains__(cls, item: Any) -> bool:
        """
        Checks whether enum contains given item

        Args:
            item (Any): Item to check.

        Returns:
            bool: True if item in enum and False otherwise.
        """
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BetterStrEnum(StrEnum, metaclass=MetaEnum):
    """
    Better StrEnum class with contains method.
    """
