import pyrr
import numpy as np

from model.entity import Entity


class BillBoard(Entity):
    """
    BillBoard entity, is always face to the camere
    """
    __slots__ = ('position', 'eulers')

    def __init__(self, position):
        """
        Initialize the billboard
        :param position: Position of the billboard in world space / scene
        """
        super().__init__(position, eulers=[0, 0, 0])

    def update(self, dt: float, camera_pos: np.ndarray) -> None:
        """
        Update the orientation of the billboard
        :param dt: Delta time
        :param camera_pos: Position of the camera in the world space / scene
        :return:
        """
        direction_from_camera = self.position - camera_pos
        self.eulers[2] = np.degrees(np.arctan2(-direction_from_camera[1], direction_from_camera[0]))
        dist = pyrr.vector.length(direction_from_camera)
        self.eulers[1] = np.degrees(np.arctan2(direction_from_camera[2], dist))
