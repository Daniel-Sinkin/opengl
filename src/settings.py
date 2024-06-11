import logging
import os
from dataclasses import dataclass

from .constants import *


@dataclass
class Physics:
    GRAVITATIONAL_CONSTANT: float = 9.81  # Accelerates in -y with G meters per second


@dataclass
class LoggingSettings:
    LEVEL: int = logging.DEBUG
    LEVEL_FILE: int = logging.INFO


@dataclass
class Settings_Camera:
    FOV: float = 60.0
    NEAR: float = 0.1
    FAR: float = 150.0
    SPEED: float = 0.01
    SPEED_TUROB: float = 0.03
    SENSITIVITY: float = 0.05

    INITIAL_POSITION: POSITION3D = (0.0, 0.0, 4.0)
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


@dataclass
class Folders:
    RECORDINGS: str = "recordings"
    RECORDINGS_CAMERA: str = os.path.join(RECORDINGS, "camera")

    SRC: str = "src"
    TEXTURES: str = "textures"
    SHADERS: str = "shaders"
    UTIL: str = "util"
    LOGS: str = "logs"
    OBJECTS: str = "objects"

    DATA: str = "data"
    DATA_SOUND: str = os.path.join(DATA, "sound")
