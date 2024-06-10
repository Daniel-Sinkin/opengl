from dataclasses import dataclass


@dataclass
class Settings_Camera:
    FOV = 60
    NEAR = 0.1
    FAR = 150.0
    SPEED = 0.01
    SENSITIVITY = 0.05


@dataclass
class Settings_OpenGL:
    WINDOW_SIZE: tuple[int, int] = (1600, 900)
    MAJOR_VERSION = 3
    MINOR_VERSION = 3


@dataclass
class Colors:
    # This should never be visible
    MISSING_TEXTURE = (1.0, 0.0, 1.0)
