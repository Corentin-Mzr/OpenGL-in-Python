from OpenGL.GL import *
from PIL import Image


class Material:
    """
    Basic texture for objects
    """
    __slots__ = ('texture',)

    def __init__(self, filepath: str):
        """
        Initialize and load the texture from a file
        :param filepath: Path to the file
        """
        # Initialize OpenGL texture
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Load texture from file
        with Image.open(filepath, mode='r') as image:
            image_width, image_height = image.size
            image = image.convert('RGBA')
            image_data = bytes(image.tobytes())
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                         image_width, image_height, 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self) -> None:
        """
        Use the texture for drawing
        """
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self) -> None:
        """
        Free the texture when not needed
        """
        glDeleteTextures(1, (self.texture,))
