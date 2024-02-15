import numpy as np

from model.entity import Entity


class Cube(Entity):
    """
    Basic cube with position and rotation
    """
    __slots__ = ('position', 'eulers')

    def __init__(self, position: list | tuple | np.ndarray, eulers: list | tuple | np.ndarray):
        """
        Initialize the cube
        :param position: Position of the cube in world space / scene
        :param eulers: Orientation of the cube in world space / scene
        """
        super().__init__(position, eulers)

    def update(self, dt: float, camera_pos: np.ndarray = None) -> None:
        """
        Update the cube
        :param dt: Delta time
        :param camera_pos: Position of the camera in world space / scene
        """
        self.eulers[2] += 0.25 * dt
        if self.eulers[2] > 360:
            self.eulers[2] -= 360
