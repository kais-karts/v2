class GoKart():
    """
    Complete state of a single Go-Kart.
    """
    def __init__(self, id: int):
        self.id = id                    #: Unique identifier for this Go-Kart (0..=5)
        self.position = (0, 0)          #: Current (x, y) position as reported by localization
        self.effect = None              #: Current effect (if any)
    
    @property
    def speed(self) -> float:
        return 1.0 if self.effect is None else self.effect.speed_multiplier