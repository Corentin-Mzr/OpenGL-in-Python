import numpy as np
from OpenGL.GL import *


class BillBoard:
    def __init__(self, w: float, h: float):
        # x, y, z, s, t, nx, ny, nz
        self.vertices = (
            0, -w / 2, h / 2, 0, 0, 1, 0, 0,
            0, -w / 2, -h / 2, 0, 1, 1, 0, 0,
            0, w / 2, -h / 2, 1, 1, 1, 0, 0,

            0, -w / 2, h / 2, 0, 0, 1, 0, 0,
            0, w / 2, -h / 2, 1, 1, 1, 0, 0,
            0, w / 2, h / 2, 1, 0, 1, 0, 0,
        )

        self.vertex_count = 6

        self.vertices = np.array(self.vertices, dtype=np.float32)

        # Vertex Array Object
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertex Buffer Object
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        # Texture coordinates
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        # Normal coordinates
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def destroy(self) -> None:
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
