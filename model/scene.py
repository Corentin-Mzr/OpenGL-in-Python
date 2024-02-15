from settings import ENTITY_TYPE

from model.entity import Entity
from model.pointlight import PointLight
from model.player import Player
from model.cube import Cube
from model.billboard import BillBoard


class Scene:
    """
    Handle objects and their interactions in the world space
    """
    __slots__ = ('entities', 'player', 'lights')

    def __init__(self):
        self.entities: dict[int, list[Entity]] = {
            ENTITY_TYPE['CUBE']: [
                Cube(position=[0, 0, 1],
                     eulers=[0, 0, 0])
            ],

            ENTITY_TYPE['MEDKIT']: [
                BillBoard(position=[0, 0, 2.5])
            ]
        }

        self.lights: list[PointLight] = [
            PointLight(position=[0, 0, 4],
                       color=[1.0, 0.0, 0.0],
                       strength=3.0),

            PointLight(position=[0.5, 0, 4],
                       color=[0.0, 1.0, 0.0],
                       strength=3.0),

            PointLight(position=[-0.5, 0, 4],
                       color=[0.0, 0.0, 1.0],
                       strength=3.0)
        ]

        self.player = Player(
            position=[-2, 0, 3]
        )

    def update(self, dt: float) -> None:
        """
        Update all objects of the scene
        :param dt: Delta time
        """
        # Update entities
        for entities in self.entities.values():
            for entity in entities:
                entity.update(dt, self.player.position)

        # Update lights
        for light in self.lights:
            light.update(dt, self.player.position)

        # Update player position
        self.player.update(dt)

    def move_player(self, dpos: list[float]) -> None:
        """
        Move the player by the given amount
        :param dpos: Displacement vector
        """
        self.player.move(dpos)

    def spin_player(self, deulers: list[float]) -> None:
        """
        Spin the player by the given amounts
        :param deulers: Euler angles displacement
        """
        self.player.spin(deulers)
