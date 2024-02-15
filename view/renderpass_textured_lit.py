import pyrr
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import ShaderProgram

from model.scene import Scene
from settings import *


class RenderPassTexturedLit3D:
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
        self.light_location = {
            "position": [glGetUniformLocation(self.shader, f"Lights[{i}].position") for i in range(8)],
            "color": [glGetUniformLocation(self.shader, f"Lights[{i}].color") for i in range(8)],
            "strength": [glGetUniformLocation(self.shader, f"Lights[{i}].strength") for i in range(8)]
        }

        self.camera_pos_loc = glGetUniformLocation(self.shader, "cameraPosition")

    def render(self, scene: Scene, engine):
        glUseProgram(self.shader)

        # View
        view_transform = pyrr.matrix44.create_look_at(eye=scene.player.position,
                                                      target=scene.player.position + scene.player.forwards,
                                                      up=scene.player.up,
                                                      dtype=np.float32)
        glUniformMatrix4fv(self.view_matrix_location, 1, GL_FALSE, view_transform)

        glUniform3fv(self.camera_pos_loc, 1, scene.player.position)

        # Lighting
        for i, light in enumerate(scene.lights):
            glUniform3fv(self.light_location['position'][i], 1, light.position)
            glUniform3fv(self.light_location['color'][i], 1, light.color)
            glUniform1f(self.light_location['strength'][i], light.strength)

        # Create cubes in scene
        for cube in scene.cubes:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(eulers=np.radians(cube.eulers), dtype=np.float32)
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(vec=cube.position, dtype=np.float32)
            )

            glUniformMatrix4fv(self.model_matrix_location, 1, GL_FALSE, model_transform)
            engine.cube_texture.use()
            glBindVertexArray(engine.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, engine.cube_mesh.vertex_count)

        # Create medkits in scene
        for medkit in scene.medkits:
            direction_from_player = medkit.position - scene.player.position
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
                m2=pyrr.matrix44.create_from_translation(vec=medkit.position, dtype=np.float32)
            )

            glUniformMatrix4fv(self.model_matrix_location, 1, GL_FALSE, model_transform)
            engine.medkit_texture.use()
            glBindVertexArray(engine.medkit_billboard.vao)
            glDrawArrays(GL_TRIANGLES, 0, engine.medkit_billboard.vertex_count)

    def destroy(self):
        glDeleteProgram(self.shader)
