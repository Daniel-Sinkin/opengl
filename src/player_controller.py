import glm
from glm import vec3

from camera import Camera
from graphics_engine import GraphicsEngine

from .constants import *


class PlayerController:
    def __init__(self, app: "GraphicsEngine", initial_position: POSITION3D = [0, 3, 0]):
        self.app: GraphicsEngine = app
        self.camera: Camera = app.camera

        self.initial_position = initial_position
        self.position = vec3(initial_position)

    def update(self):
        if self.app.player_controller_mode:
            self.camera.position = self.position

            p
