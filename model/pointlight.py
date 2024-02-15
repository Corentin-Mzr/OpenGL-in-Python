import numpy as np

from model.billboard import BillBoard


class PointLight(BillBoard):
    """
    Simple point light
    """
    __slots__ = ('position', 'eulers', 'color', 'strength')

    def __init__(self, position: list | tuple | np.ndarray, color: list | tuple | np.ndarray, strength: float):
        """
        Initialize the light
        :param position: Position of the light in the scene
        :param color: Color of the light as (r,g,b) tuple
        :param strength: Strength of the light
        """
        super().__init__(position)
        self.color = np.array(color, dtype=np.float32)
        self.strength = strength
