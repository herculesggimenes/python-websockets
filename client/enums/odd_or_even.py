from enum import Enum


class OddOrEven(Enum):
    ODD='odd'
    EVEN='even'

    @classmethod
    def has_value(self, value):
        return value in self._value2member_map_