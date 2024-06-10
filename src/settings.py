from dataclasses import dataclass


@dataclass
class Settings:
    @dataclass
    class Camera:
        FOV = 60
        NEAR = 0.1
        FAR = 150.0
        SPEED = 0.01
        SENSITIVITY = 0.05
