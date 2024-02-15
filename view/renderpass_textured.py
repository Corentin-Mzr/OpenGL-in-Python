import pyrr
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import ShaderProgram

from settings import *
from model.scene import Scene


class RenderPassTextured3D:
    def __init__(self, shader: ShaderProgram):
        # Initialization
        self.shader = shader
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        # Define projection and other uniforms
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WIDTH / HEIGHT,
            near=0.1, far=10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

        self.model_matrix_location = glGetUniformLocation(self.shader, "model")
        self.view_matrix_location = glGetUniformLocation(self.shader, "view")

        self.tint_loc = glGetUniformLocation(self.shader, "tint")

    def render(self, scene: Scene, engine):
        glUseProgram(self.shader)

        # View
        view_transform = pyrr.matrix44.create_look_at(eye=scene.player.position,
                                                      target=scene.player.position + scene.player.forwards,
                                                      up=scene.player.up,
                                                      dtype=np.float32)
        glUniformMatrix4fv(self.view_matrix_location, 1, GL_FALSE, view_transform)

        # Create lights billboard in the scene
        for i, light in enumerate(scene.lights):
            glUniform3fv(self.tint_loc, 1, light.color)

            direction_from_player = light.position - scene.player.position
            angle1 = np.arctan2(-direction_from_player[1], direction_from_player[0])
            dist = np.sqrt(direction_from_player[0] ** 2 + direction_from_player[1] ** 2)
            angle2 = np.arctan2(direction_from_player[2], dist)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_y_rotation(theta=angle2, dtype=np.float32)
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_z_rotation(theta=angle1, dtype=np.float32)
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(vec=light.position, dtype=np.float32)
            )
            glUniformMatrix4fv(self.model_matrix_location, 1, GL_FALSE, model_transform)

            engine.light_texture.use()
            glBindVertexArray(engine.light_billboard.vao)
            glDrawArrays(GL_TRIANGLES, 0, engine.light_billboard.vertex_count)

    def destroy(self):
        glDeleteProgram(self.shader)
