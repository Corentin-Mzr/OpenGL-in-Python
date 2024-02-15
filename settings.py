import numpy as np

WIDTH: int = 800
HEIGHT: int = 600
TITLE: str = "OpenGL with Python"

BG_RED: float = 0.0
BG_GREEN: float = 0.0
BG_BLUE: float = 0.0

RETURN_ACTION_CONTINUE: int = 0
RETURN_ACTION_END: int = 1

RATE: float = 1000.0 / 144.0

GLOBAL_X: np.ndarray = np.array([1, 0, 0], dtype=np.float32)
GLOBAL_Y: np.ndarray = np.array([0, 1, 0], dtype=np.float32)
GLOBAL_Z: np.ndarray = np.array([0, 0, 1], dtype=np.float32)

ENTITY_TYPE: dict[str, int] = {
    "CUBE": 0,
    "POINTLIGHT": 1,
    "MEDKIT": 2,
}

UNIFORM_TYPE: dict[str, int] = {
    "MODEL": 0,
    "VIEW": 1,
    "PROJECTION": 2,
    "CAMERA_POS": 3,
    "LIGHT_COLOR": 4,
    "LIGHT_POS": 5,
    "LIGHT_STRENGTH": 6,
    "TINT": 7,
}

PIPELINE_TYPE: dict[str, int] = {
    "STANDARD": 0,
    "EMISSIVE": 1,
}
