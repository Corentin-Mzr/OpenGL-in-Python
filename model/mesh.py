from OpenGL.GL import *


class Mesh:
    """
    Basic mesh
    """
    __slots__ = ('vao', 'vbo', 'vertex_count')

    def __init__(self):
        """
        Initialize the mesh
        """
        # Vertex Array Object
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertex Buffer Object
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        # Texture coordinates
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        # Normal coordinates
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def arm_for_drawing(self) -> None:
        """
        Arm the triangle for drawing
        """
        glBindVertexArray(self.vao)

    def draw(self) -> None:
        """
        Draw the triangle
        """
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self) -> None:
        """
        Free the memory
        """
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
