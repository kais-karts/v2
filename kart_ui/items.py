from dataclasses import dataclass
from enum import Enum
from typing import List

class ItemEffect(Enum):
    BUFF = "buff"
    DEBUFF = "debuff"

class ItemTarget(Enum):
    SELF = "self"
    FRONT = "front"
    BEHIND = "behind"
    ALL_OTHERS = "all_others"
    LEADER = "leader"

@dataclass
class Item:
    name: str
    effect: ItemEffect
    target: ItemTarget
    speed_multiplier: float
    duration: int
    distribution: List[int]

ITEMS = [
    Item(
        "banana", 
        ItemEffect.DEBUFF, 
        ItemTarget.BEHIND, 
        0, 
        3, 
        [30, 20, 20, 0, 0, 0]
    ),
    Item(
        "bomb", 
        ItemEffect.DEBUFF, 
        ItemTarget.ALL_OTHERS, 
        0, 
        10, 
        [0, 0, 10, 15, 15, 0]
    ),
    Item(
        "redShroom", 
        ItemEffect.BUFF, 
        ItemTarget.SELF, 
        0.75, 
        5, 
        [30, 25, 50, 30, 10, 0]
    ),
    Item(
        "goldShroom", 
        ItemEffect.BUFF, 
        ItemTarget.SELF, 
        0.75, 
        10, 
        [0, 0, 0, 10, 50, 50]
    ),
    Item(
        "redShell", 
        ItemEffect.DEBUFF, 
        ItemTarget.FRONT, 
        0, 
        5, 
        [0, 30, 30, 20, 10, 0]
    ),
    Item(
        "blueShell", 
        ItemEffect.DEBUFF, 
        ItemTarget.LEADER, 
        0, 
        7, 
        [0, 0, 10, 20, 10, 0]
    ),
    Item(
        "lightning", 
        ItemEffect.DEBUFF, 
        ItemTarget.ALL_OTHERS, 
        0.25, 
        5, 
        [0, 0, 0, 5, 10, 10]
    ),
    Item(
        "bulletBill", 
        ItemEffect.BUFF, 
        ItemTarget.SELF, 
        1, 
        10, 
        [0, 0, 0, 0, 0, 50]
    )
]