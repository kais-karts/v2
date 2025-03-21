from constants import KART_ID
from kart_ui.map import Map


class GoKart():
    """
    Complete state of a single Go-Kart.

    Attributes:
        id (int): Unique identifier for this kart.
        position (tuple[float, float] | None): 2D location on the track, or `None` if not yet known.
        laps (int): Number of laps completed by this kart.
        speed_multiplier (float): Multiplier for the kart's speed (default 1.0).
    """
    def __init__(self, id: int, game_map: Map):
        self._id = id
        self._game_map = game_map
        self._position = None
        self._laps = 0
        self.speed_multiplier = 1.0

    def __gt__(self, other) -> bool:
        """
        Check if this kart is ahead of another kart
        """
        if not isinstance(other, GoKart):
            return NotImplemented
        return (self._laps > other.laps) or (self._laps == other.laps and self._position > other.position)

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
        # check for irregular movement
        # check for kart passing finish line
        # check for kart passing item_checkpoint
        self._position = val

    @property
    def laps(self) -> int:
        """
        Number of laps completed by this kart
        """
        return self._laps