import pyrr
import numpy as np

from model.entity import Entity
from settings import GLOBAL_Z


class Player(Entity):
    """
    A player entity
    """
    __slots__ = ('position', 'eulers', 'forwards', 'right', 'up', 'velocity', 'sensitivity')

    def __init__(self, position: list | tuple | np.ndarray, velocity: float = 0.005, sensitivity: float = 0.2):
        """
        Initialize the player
        :param position: Position of the player in the scene
        """
        super().__init__(position, eulers=[0, 0, 0])

        self.velocity = velocity
        self.sensitivity = sensitivity
        self.forwards = None
        self.right = None
        self.up = None

    def update(self, dt: float, camera_pos: np.ndarray = None) -> None:
        """
        Update the player's camera
        :param dt: Delta time
        :param camera_pos: Camera position (unused)
        """
        theta = self.eulers[2]
        phi = self.eulers[1]

        self.forwards = np.array(
            [
                np.cos(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),
                np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),
                np.sin(np.deg2rad(phi))
            ],
            dtype=np.float32)

        self.right = np.cross(self.forwards, GLOBAL_Z)
        self.up = np.cross(self.right, self.forwards)

    def get_view_transform(self) -> np.ndarray:
        """
        Returns the view transformation matrix
        """
        view_transform = pyrr.matrix44.create_look_at(
            eye=self.position,
            target=self.position + self.forwards,
            up=self.up,
            dtype=np.float32
        )
        return view_transform

    def move(self, dpos: list | tuple | np.ndarray) -> None:
        """
        Move the player by the given amount
        :param dpos: Displacement vector
        """
        self.position += dpos[0] * self.forwards + dpos[1] * self.right + dpos[2] * self.up

        self.position[2] = 3

    def spin(self, deulers: list | tuple | np.ndarray) -> None:
        self.eulers += deulers

        self.eulers[0] %= 360
        self.eulers[1] = min(89.0, max(-89.0, self.eulers[1]))
        self.eulers[2] %= 360
