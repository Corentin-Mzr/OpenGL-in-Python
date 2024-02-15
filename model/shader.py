from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram, ShaderProgram


class Shader:
    """
    A shader
    """
    __slots__ = ('program', 'single_uniforms', 'multi_uniforms')

    def __init__(self, vertex_filepath: str, fragment_filepath: str):
        """
        Initialize the shader
        :param vertex_filepath: Path to the vertex file
        :param fragment_filepath: Path to the fragment file
        """
        self.program = self.create_shader(vertex_filepath, fragment_filepath)

        self.single_uniforms: dict[int, int] = {}
        self.multi_uniforms: dict[int, list[int]] = {}

    @staticmethod
    def create_shader(vertex_filepath: str, fragment_filepath: str) -> ShaderProgram:
        """
        Returns the shader program for the given vertex and fragment filepath
        :param vertex_filepath: Path to the vertex file
        :param fragment_filepath: Path to the fragment file
        """
        with open(vertex_filepath, "r") as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, "r") as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def cache_single_location(self, uniform_type: int, uniform_name: str) -> None:
        """
        Store location of a uniform location, for uniforms with one location per variable
        :param uniform_type: Type of uniform
        :param uniform_name: Name of the uniform
        """
        self.single_uniforms[uniform_type] = glGetUniformLocation(self.program, uniform_name)

    def cache_multi_location(self, uniform_type: int, uniform_name: str) -> None:
        """
        Search location of a uniform location, for uniforms with multiple locations per variable
        :param uniform_type: Type of uniform
        :param uniform_name: Name of the uniform
        """
        # Create the list if uniform not in dict yet
        if uniform_type not in self.multi_uniforms:
            self.multi_uniforms[uniform_type] = []

        self.multi_uniforms[uniform_type].append(
            glGetUniformLocation(self.program, uniform_name)
        )

    def fetch_single_location(self, uniform_type: int) -> int:
        """
        Returns the location of the uniform location, for uniforms with one location per variable
        :param uniform_type: Type of uniform to retrieve
        """
        return self.single_uniforms[uniform_type]

    def fetch_multi_location(self, uniform_type: int, index: int) -> int:
        """
        Returns the location of the uniform location, for uniforms with multiple locations per variable
        :param uniform_type: Type of uniform to retrieve
        :param index: Index of the uniform
        """
        return self.multi_uniforms[uniform_type][index]

    def use(self) -> None:
        """
        Use the shader program
        """
        glUseProgram(self.program)

    def destroy(self) -> None:
        """
        Free the memory
        """
        glDeleteProgram(self.program)
