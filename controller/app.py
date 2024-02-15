import pyrr

import glfw
import glfw.GLFW as GLFW_CONSTANTS

from OpenGL.GL import *

from settings import *
from view.graphics_engine import GraphicsEngine
from model.scene import Scene


class App:
    """
    Controller class
    """
    __slots__ = ('window', 'renderer', 'scene', 'last_time', 'current_time', 'fps', 'frame_time', '_keys')

    def __init__(self):
        """
        Initialize the program
        """
        self._set_up_glfw()

        self._set_up_timer()

        self._set_up_input_mode()

        self._create_assets()

    def _set_up_glfw(self) -> None:
        """
        Initialize and configure GLFW
        """
        # Basic initialization
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

        # Create the window
        self.window = glfw.create_window(WIDTH, HEIGHT, TITLE, None, None)
        glfw.make_context_current(self.window)

    def _set_up_timer(self) -> None:
        """
        Initialize variables for framerate
        """
        self.last_time = glfw.get_time()
        self.current_time = 0
        self.fps = 0
        self.frame_time = 0

    def _set_up_input_mode(self) -> None:
        """
        Configure mouse and keyboard
        """
        glfw.set_input_mode(
            self.window,
            GLFW_CONSTANTS.GLFW_CURSOR,
            GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
        )

        self._keys = {}
        glfw.set_key_callback(self.window, self._key_callback)

    def _key_callback(self, window, key, scancode, action, mode) -> None:
        """
        Handle key events
        :param window: Window on which the key is pressed
        :param key: Key pressed
        :param scancode: Scancode of the key
        :param action: Action of the key event
        :param mode: Modifiers applied to the event
        """
        match action:
            case GLFW_CONSTANTS.GLFW_PRESS:
                state = True
            case GLFW_CONSTANTS.GLFW_RELEASE:
                state = False
            case _:
                return None

        self._keys[key] = state

    def _create_assets(self) -> None:
        """
        Create assets needed by the program
        """
        self.renderer = GraphicsEngine()

        self.scene = Scene()

    def run(self) -> None:
        """
        Run the program
        """
        running = True

        while running:
            if (glfw.window_should_close(self.window)
                    or glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS):
                running = False

            self._handle_keys()
            self._handle_mouse()

            glfw.poll_events()

            self.scene.update(self.frame_time / RATE)
            self.renderer.render(self.scene.player, self.scene.entities, self.scene.lights)

            # FPS
            self._compute_framerate()

    def _handle_keys(self) -> None:
        """
        Take action based on key pressed
        """
        rate = self.scene.player.velocity * self.frame_time
        dpos = np.zeros(3, dtype=np.float32)

        if self._keys.get(GLFW_CONSTANTS.GLFW_KEY_W, False):
            dpos += GLOBAL_X
        if self._keys.get(GLFW_CONSTANTS.GLFW_KEY_A, False):
            dpos -= GLOBAL_Y
        if self._keys.get(GLFW_CONSTANTS.GLFW_KEY_S, False):
            dpos -= GLOBAL_X
        if self._keys.get(GLFW_CONSTANTS.GLFW_KEY_D, False):
            dpos += GLOBAL_Y

        length = pyrr.vector.length(dpos)

        if abs(length) < 0.00001:
            return None

        dpos = 0.005 * RATE * dpos / length

        self.scene.move_player(dpos)

    def _handle_mouse(self) -> None:
        """
        Orientate the player based on mouse movement
        """
        x, y = glfw.get_cursor_pos(self.window)
        deulers = self.scene.player.sensitivity * ((WIDTH / 2) - x) * GLOBAL_Z
        deulers += self.scene.player.sensitivity * ((HEIGHT / 2) - y) * GLOBAL_Y
        self.scene.spin_player(deulers)
        glfw.set_cursor_pos(self.window, WIDTH / 2, HEIGHT / 2)

    def _compute_framerate(self) -> None:
        """
        Calculate the framerate and the frametime, FPS is shown on the window title
        """
        self.current_time = glfw.get_time()
        delta_time = self.current_time - self.last_time
        if delta_time >= 1.0:
            framerate = max(1.0, int(self.fps / delta_time))
            glfw.set_window_title(self.window, f'{TITLE} | FPS : {framerate:.0f}')
            self.last_time = self.current_time
            self.fps = -1
            self.frame_time = 1000.0 / max(1.0, framerate)
        self.fps += 1

    def quit(self) -> None:
        self.renderer.quit()
