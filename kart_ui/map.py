from typing import Tuple

class Map:
    """
    Represents the race track and all location-based logic.

    Attributes:
        start_line (Tuple[float, float]): Coordinates of the start/finish line
        item_checkpoints (List[Tuple[float, float]]): List of item pickup zones
        track_path (List[Tuple[float, float]]): Ordered list of "ideal line" points
    """
    def __init__(self, start_line: tuple[float, float], item_checkpoints: list[tuple[float, float]], track_path: list[tuple[float, float]]):
        self._start_line = start_line
        self._item_checkpoints = item_checkpoints
        self._track_path = track_path

    def is_valid_movement(self, last_pos, curr_pos) -> bool:
        """Check if a kart's movement is valid."""
        return NotImplementedError

    def crossed_finish_line(self, last_pos, curr_pos) -> bool:
        """Detect if kart just crossed the start/finish line."""
        return NotImplementedError

    def get_track_index(self, position: Tuple[float, float]) -> int:
        """Convert a 2D position into a progress index along the track."""
        return NotImplementedError

    def is_within_item_checkpoint(self, position) -> bool:
        """Check if position is within any item checkpoint."""
        return NotImplementedError