import pyrr

from OpenGL.GL import *

from model.rect_mesh import RectMesh
from settings import *
from model.obj_mesh import ObjMesh
from model.material import Material
from model.player import Player
from model.entity import Entity
from model.pointlight import PointLight
from model.shader import Shader


class GraphicsEngine:
    """
    Draw entities
    """
    __slots__ = ('meshes', 'materials', 'shaders')

    def __init__(self):
        self._set_up_opengl()

        self._create_assets()

        self._set_onetime_uniforms()

        self._get_uniform_locations()

    @staticmethod
    def _set_up_opengl() -> None:
        """
        Initialize OpenGL
        """
        glClearColor(BG_RED, BG_GREEN, BG_BLUE, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _create_assets(self) -> None:
        """
        Create all the assets to draw
        """
        # Create resources and shaders
        self.meshes: dict[int, ObjMesh] = {
            ENTITY_TYPE['CUBE']: ObjMesh('objects/cube.obj'),
            ENTITY_TYPE['MEDKIT']: RectMesh(w=0.6, h=0.5),
            ENTITY_TYPE['POINTLIGHT']: RectMesh(w=0.2, h=0.1),

        }

        self.materials: dict[int, Material] = {
            ENTITY_TYPE['CUBE']: Material('textures/wood.jpg'),
            ENTITY_TYPE['MEDKIT']: Material('textures/medkit.png'),
            ENTITY_TYPE['POINTLIGHT']: Material('textures/light.png'),
        }

        self.shaders: dict[int, Shader] = {
            PIPELINE_TYPE['STANDARD']: Shader(
                'shaders/vertex.vert',
                'shaders/fragment.frag'
            ),
            PIPELINE_TYPE['EMISSIVE']: Shader(
                'shaders/vertex_light.vert',
                'shaders/fragment_light.frag'
            )
        }

    def _set_onetime_uniforms(self) -> None:
        """
        Sets up the data once when needed
        """
        # Define projection and other uniforms
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WIDTH / HEIGHT,
            near=0.1, far=10, dtype=np.float32
        )

        for shader in self.shaders.values():
            shader.use()
            glUniform1i(glGetUniformLocation(shader.program, "imageTexture"), 0)
            glUniformMatrix4fv(
                glGetUniformLocation(shader.program, "projection"),
                1, GL_FALSE, projection_transform
            )

    def _get_uniform_locations(self) -> None:
        """
        Store the location of shader uniforms
        """
        shader = self.shaders[PIPELINE_TYPE['STANDARD']]
        shader.use()

        shader.cache_single_location(UNIFORM_TYPE['CAMERA_POS'], 'cameraPosition')
        shader.cache_single_location(UNIFORM_TYPE['MODEL'], 'model')
        shader.cache_single_location(UNIFORM_TYPE['VIEW'], 'view')

        for i in range(8):
            shader.cache_multi_location(
                UNIFORM_TYPE['LIGHT_COLOR'], f'Lights[{i}].color'
            )
            shader.cache_multi_location(
                UNIFORM_TYPE['LIGHT_POS'], f'Lights[{i}].position'
            )
            shader.cache_multi_location(
                UNIFORM_TYPE['LIGHT_STRENGTH'], f'Lights[{i}].strength'
            )

        shader = self.shaders[PIPELINE_TYPE['EMISSIVE']]
        shader.use()

        shader.cache_single_location(UNIFORM_TYPE['MODEL'], 'model')
        shader.cache_single_location(UNIFORM_TYPE['VIEW'], 'view')
        shader.cache_single_location(UNIFORM_TYPE['TINT'], 'tint')

    def render(self, player: Player, entities: dict[int, list[Entity]], lights: list[PointLight]) -> None:
        """
        Draw everything on the screen
        :param player: The camera
        :param entities: Every entity to draw
        :param lights: Every light in the scene
        """
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw
        view = player.get_view_transform()
        shader = self.shaders[PIPELINE_TYPE['STANDARD']]
        shader.use()

        glUniformMatrix4fv(
            shader.fetch_single_location(UNIFORM_TYPE['VIEW']),
            1,
            GL_FALSE,
            view
        )

        glUniform3fv(
            shader.fetch_single_location(UNIFORM_TYPE['CAMERA_POS']),
            1,
            player.position
        )

        # Standard Lighting
        for i, light in enumerate(lights):
            glUniform3fv(
                shader.fetch_multi_location(UNIFORM_TYPE['LIGHT_POS'], i),
                1,
                light.position
            )
            glUniform3fv(
                shader.fetch_multi_location(UNIFORM_TYPE['LIGHT_COLOR'], i),
                1,
                light.color
            )
            glUniform1f(shader.fetch_multi_location(
                UNIFORM_TYPE['LIGHT_STRENGTH'], i),
                light.strength
            )

        # Entities
        for entity_type, ent in entities.items():
            if entity_type not in self.materials:
                continue

            material = self.materials[entity_type]
            material.use()
            mesh = self.meshes[entity_type]
            mesh.arm_for_drawing()

            for entity in ent:
                glUniformMatrix4fv(
                    shader.fetch_single_location(UNIFORM_TYPE['MODEL']),
                    1,
                    GL_FALSE,
                    entity.get_model_transform()
                )

                mesh.draw()

        # Emissive lighting
        shader = self.shaders[PIPELINE_TYPE['EMISSIVE']]
        shader.use()

        glUniformMatrix4fv(
            shader.fetch_single_location(UNIFORM_TYPE['VIEW']),
            1, GL_FALSE,
            view
        )

        material = self.materials[ENTITY_TYPE['POINTLIGHT']]
        material.use()
        mesh = self.meshes[ENTITY_TYPE['POINTLIGHT']]
        mesh.arm_for_drawing()

        for light in lights:
            glUniform3fv(
                shader.fetch_single_location(UNIFORM_TYPE['TINT']),
                1,
                light.color
            )
            glUniformMatrix4fv(
                shader.fetch_single_location(UNIFORM_TYPE['MODEL']),
                1,
                GL_FALSE,
                light.get_model_transform()
            )

            mesh.draw()

        # Display
        glFlush()

    def quit(self) -> None:
        """
        Free allocated memory
        """
        for mesh in self.meshes.values():
            mesh.destroy()
        for material in self.materials.values():
            material.destroy()
        for shader in self.shaders.values():
            shader.destroy()
