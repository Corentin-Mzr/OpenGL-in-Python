import pyrr
import numpy as np


class Entity:
    """
    Basic object with a position and a rotation
    """
    __slots__ = ('position', 'eulers')

    def __init__(self, position: tuple | list | np.ndarray, eulers: tuple | list | np.ndarray):
        """
        Initialize the entity
        :param position: Position of the entity in the world space / scene
        :param eulers: Orientation of the entity in the world space / scene
        """
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

    def update(self, dt: float, camera_pos: np.ndarray) -> None:
        """
        Update the object position and orientation, this is implemented for subclasses of this class
        :param dt: Delta time
        :param camera_pos: Position of the camera in world space / scene
        """
        pass

    def get_model_transform(self) -> np.ndarray:
        """
        Returns the entity transformation matrix
        """
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_y_rotation(
                theta=np.deg2rad(self.eulers[1]),
                dtype=np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_z_rotation(
                theta=np.deg2rad(self.eulers[2]),
                dtype=np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_translation(
                vec=self.position,
                dtype=np.float32
            )
        )

        return model_transform
