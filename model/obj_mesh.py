import numpy as np
from OpenGL.GL import *

from model.mesh import Mesh


class ObjMesh(Mesh):
    """
    Basic mesh initialized from OBJ file
    """
    __slots__ = ('vao', 'vbo', 'vertex_count')

    def __init__(self, filepath: str):
        """
        Initialize the mesh
        :param filepath: Path to the file
        """
        super().__init__()

        # x, y, z, s, t, nx, ny, nz
        vertices = self.load_mesh(filepath)
        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    def load_mesh(self, filepath: str) -> list[float]:
        v = []
        vt = []
        vn = []

        vertices = []
        with open(filepath, 'r') as f:
            line = f.readline()
            while line:
                words = line.split(' ')
                if words[0] == 'v':
                    v.append(self.read_data(words))
                if words[0] == 'vt':
                    vt.append(self.read_data(words))
                if words[0] == 'vn':
                    vn.append(self.read_data(words))
                if words[0] == 'f':
                    self.read_face_data(words, v, vt, vn, vertices)
                line = f.readline()

        return vertices

    @staticmethod
    def read_data(words: list[str]) -> list[float]:
        return [float(w) for w in words[1:]]

    @staticmethod
    def read_face_data(words: list[str],
                       v: list[list[float]],
                       vt: list[list[float]],
                       vn: list[list[float]],
                       vertices: list[float]) -> None:
        for w in words[1:]:
            idx = [int(e) - 1 for e in w.split('/')]

            for element in v[idx[0]]:
                vertices.append(element)

            for element in vt[idx[1]]:
                vertices.append(element)

            for element in vn[idx[2]]:
                vertices.append(element)
