import numpy as np

from OpenGL.GL import *

from model.mesh import Mesh


class RectMesh(Mesh):
    """
    A rectangular mesh
    """

    __slots__ = ('vao', 'vbo', 'vertex_count')

    def __init__(self, w: float, h: float):
        """
        Initialize the rectangle mesh with the given width and height
        :param w: Width of the mesh
        :param h: Height of the mesh
        """
        super().__init__()
        # x, y, z, s, t, nx, ny, nz
        vertices = (
            0, -w / 2, h / 2, 0, 0, 1, 0, 0,
            0, -w / 2, -h / 2, 0, 1, 1, 0, 0,
            0, w / 2, -h / 2, 1, 1, 1, 0, 0,

            0, -w / 2, h / 2, 0, 0, 1, 0, 0,
            0, w / 2, -h / 2, 1, 1, 1, 0, 0,
            0, w / 2, h / 2, 1, 0, 1, 0, 0,
        )

        self.vertex_count = 6
        vertices = np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)