from constants import KART_ID


class GoKart():
    """
    Complete state of a single Go-Kart
    """
    def __init__(self, id: int):
        self._id = id
        self._position = None       # Unknown
        self.speed_multiplier = 1.0

    @property
    def id(self) -> int:
        """
        Unique identifier for this kart (0..=7)
        """
        return self._id
    
    @property
    def is_owned(self) -> bool:
        """
        Does this Go-Kart object refer to the go-kart running this code rn?
        """
        return self._id == KART_ID
    
    @property
    def position(self) -> tuple[float, float] | None:
        """
        2D location on the track, or `None` is not yet known
        """
        return self._position
    
    @position.setter
    def position(self, val):
        self._position = val