import numpy as np
from OpenGL.GL import *


class CubeMesh:
    def __init__(self):
        # x, y, z, r, g, b, s, t
        self.vertices = (
            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 0.0,
            0.5, -0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0,
            0.5, 0.5, -0.5, 0.0, 0.0, 1.0, 1.0, 1.0,

            0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 0.0,

            -0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0,
            0.5, -0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 0.0,
            0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 1.0,

            0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0,

            -0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,
            -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 0.0,
            -0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 0.0,

            0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,
            0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 1.0,
            0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0,

            0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0, 1,
            0.5, -0.5, 0.5, 0.0, 1.0, 0.0, 0, 0,
            0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1, 0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0, 1,
            0.5, -0.5, -0.5, 0.0, 1.0, 0.0, 1, 1,
            0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 1, 0,

            0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 1, 0,
            -0.5, -0.5, 0.5, 0.0, 1.0, 0.0, 0, 0,
            -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 0, 1,

            -0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 0, 1,
            0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1, 1,
            0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1, 0,

            0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1, 0,
            -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0, 0,
            -0.5, 0.5, -0.5, 0.0, 0.0, 1.0, 0, 1
        )

        self.vertex_count = len(self.vertices) // 8

        # Convert to numpy array to be readable by OpenGL
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

        # Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        # Texture coordinates
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))

    def destroy(self) -> None:
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
