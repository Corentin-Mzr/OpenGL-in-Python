import numpy as np

from settings import ENTITY_TYPE

from model.entity import Entity
from model.pointlight import PointLight
from model.player import Player
from model.cube import Cube
from model.billboard import BillBoard


class Scene:
    __slots__ = ('entities', 'player', 'lights')

    def __init__(self):
        self.entities = {
            ENTITY_TYPE['CUBE']: [
                Cube(position=[0, 0, 1],
                     eulers=[0, 0, 0])
            ]
        }

        self.cubes = [
            Cube(position=[0, 0, 1],
                 eulers=[0, 0, 0])
        ]

        self.medkits = [
            Entity(
                position=[0, 0, 2.5],
                eulers=[0, 0, 0]
            ),
        ]

        self.lights = [
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

        self.player = Player(position=[-2, 0, 3])

    def update(self, rate: float) -> None:
        for cube in self.cubes:
            cube.update(rate)

    def move_player(self, dpos: list[float]) -> None:
        dpos = np.array(dpos, dtype=np.float32)
        self.player.position += dpos

    def spin_player(self, dtheta: float, dphi: float) -> None:
        self.player.theta += dtheta
        if self.player.theta > 360:
            self.player.theta -= 360
        if self.player.theta < 0:
            self.player.theta += 360

        self.player.phi = min(89.0, max(self.player.phi + dphi, -89.0))

        self.player.update()
