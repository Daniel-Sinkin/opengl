from dataclasses import dataclass

from .constants import *


@dataclass
class Settings_Camera:
    FOV: float = 60.0
    NEAR: float = 0.1
    FAR: float = 150.0
    SPEED: float = 0.01
    SENSITIVITY: float = 0.05

    INITIAL_POSITION: POINT = (0.0, 0.0, 4.0)
    INITIAL_YAW: float = -90.0
    INITAL_PITCH: float = 16.0

    PITCH_BOUNDS: tuple[float, float] = (-89.0, 89.0)
    FOV_BOUNDS: tuple[float, float] = (50.0, 100.0)


@dataclass
class Settings_OpenGL:
    WINDOW_SIZE: tuple[int, int] = (1600, 900)
    MAJOR_VERSION: int = 3
    MINOR_VERSION: int = 3


@dataclass
class Colors:
    # This should never be visible
    MISSING_TEXTURE: tuple[float, float, float] = (1.0, 0.0, 1.0)
