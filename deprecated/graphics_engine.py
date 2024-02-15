import pyrr
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram, ShaderProgram

from settings import *
from model.obj_mesh import ObjMesh
from model.material import Material
from model.scene import Scene
from model.billboard import BillBoard


class GraphicsEngine:
    def __init__(self):
        # Initialize OpenGL
        glClearColor(BG_RED, BG_GREEN, BG_BLUE, 1.0)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Create shader and resources
        self.shader = self.create_shader("shaders/vertex.vert", "shaders/fragment.frag")
        glUseProgram(self.shader)

        # Textures
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        # Import objects of the scene
        self.cube_mesh = ObjMesh("objects/cube.obj")
        self.cube_texture = Material("textures/wood.jpg")

        self.medkit_texture = Material("textures/medkit.png")
        self.medkit_billboard = BillBoard(w=0.6, h=0.5)

        self.light_texture = Material("textures/light.png")
        self.light_billboard = BillBoard(w=0.2, h=0.1)

        # Projection
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
        self.tint_loc = glGetUniformLocation(self.shader, "tint")

    @staticmethod
    def create_shader(vertex_filepath: str, fragment_filepath: str) -> ShaderProgram:
        with open(vertex_filepath, "r") as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, "r") as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def render(self, scene: Scene) -> None:
        # Clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw elements of the scene
        glUseProgram(self.shader)

        # View
        view_transform = pyrr.matrix44.create_look_at(eye=scene.player.position,
                                                      target=scene.player.position + scene.player.forwards,
                                                      up=scene.player.up,
                                                      dtype=np.float32)
        glUniformMatrix4fv(self.view_matrix_location, 1, GL_FALSE, view_transform)

        # Lighting
        for i, light in enumerate(scene.lights):
            glUniform3fv(self.light_location['position'][i], 1, light.position)
            glUniform3fv(self.light_location['color'][i], 1, light.color)
            glUniform1f(self.light_location['strength'][i], light.strength)
        glUniform3fv(self.camera_pos_loc, 1, scene.player.position)

        # Create lights billboard in the scene
        for light in scene.lights:
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
            self.light_texture.use()
            glBindVertexArray(self.light_billboard.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.light_billboard.vertex_count)

        glUniform3fv(self.tint_loc, 1, np.array([1.0, 1.0, 1.0], dtype=np.float32))

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
            self.cube_texture.use()
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

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
            self.medkit_texture.use()
            glBindVertexArray(self.medkit_billboard.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.medkit_billboard.vertex_count)

        # Display
        glFlush()

    def quit(self) -> None:
        self.cube_mesh.destroy()
        self.cube_texture.destroy()

        self.medkit_billboard.destroy()
        self.medkit_texture.destroy()

        self.light_billboard.destroy()
        self.light_texture.destroy()
        glDeleteProgram(self.shader)