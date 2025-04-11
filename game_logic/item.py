from aenum import AutoNumberEnum
from enum import Enum, auto


class Target(Enum):
    SELF = auto()
    FRONT = auto()
    BEHIND = auto()
    ALL_OTHERS = auto()
    LEADER = auto()
    CHECK_POINT = auto()

class Item(AutoNumberEnum):
    _init_ = "target speed_multiplier duration distribution"

    # name    |       target       |  speed  |  time  |  distribution
    BANANA      = Target.CHECK_POINT,   0.0,    3.0,    [30, 20, 20, 0, 0, 0]
    BOMB        = Target.ALL_OTHERS,    0.0,    10.0,   [0, 0, 10, 15, 15, 0]
    RED_SHROOM  = Target.SELF,          1.5,    5.0,    [30, 25, 50, 30, 10, 0]
    GOLD_SHROOM = Target.SELF,          1.5,    10.0,   [0, 0, 0, 10, 50, 50]
    RED_SHELL   = Target.FRONT,         0.0,    5.0,    [0, 30, 30, 20, 10, 0]
    BLUE_SHELL  = Target.LEADER,        0.0,    7.0,    [0, 0, 10, 20, 10, 0]
    LIGHTNING   = Target.ALL_OTHERS,    0.5,    5.0,    [0, 0, 0, 5, 10, 10]
    BULLET_BILL = Target.SELF,          2.0,    10.0,   [0, 0, 0, 0, 0, 50]

    @property
    def file_name(self) -> str:
        return self.name.lower()