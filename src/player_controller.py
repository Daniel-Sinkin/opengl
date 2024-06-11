import logging
import typing
from logging import Logger

import glm
import pygame as pg
from glm import vec3
from pygame.key import ScancodeWrapper

from . import my_logger
from .camera import Camera
from .constants import *

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine


class PlayerController:
    def __init__(self, app: "GraphicsEngine", initial_position: POSITION3D = (0, 3, 0)):
        self.logger: Logger = my_logger.setup("PlayerController")
        self.logger.setLevel(logging.DEBUG)

        self.app: GraphicsEngine = app
        self.camera: Camera = app.camera

        self.initial_position = initial_position
        self.position = vec3(initial_position)

        self.camera_offset: vec3 = vec3_y

        self.forward: vec3 = glm.normalize(
            vec3(self.camera.forward.x, 0, self.camera.forward.z)
        )
        self.right: vec3 = vec3(-self.forward.z, 0, self.forward.x)

        # TODO: Add to settings
        self.speed = 0.01
        self.speed_turbo = 0.03

    def update(self) -> None:
        if self.app.player_controller_mode == PLAYER_CONTROLLER_MODE.FPS:
            self.camera.position = self.position + self.camera_offset

            self.forward: vec3 = glm.normalize(
                vec3(self.camera.forward.x, 0, self.camera.forward.z)
            )
            # glm.cross(self.foward, vec3_y) == (vx, 0, vz) x (0, 1, 0) == (-vz, 0, vx)
            self.right: vec3 = vec3(-self.forward.z, 0, self.forward.x)

            self.logger.debug(
                "forward=(%.3f, %.3f, %.3f), right=(%.3f, %.3f, %.3f)",
                *self.forward,
                *self.right
            )

    def move(self) -> None:
        """
        When controlling a floating camera we can just pass through objects so we
        don't need any bound checks.
        """
        keys: ScancodeWrapper = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            pass

        if keys[pg.K_LSHIFT]:
            velocity: float = self.speed_turbo * self.app.delta_time
        else:
            velocity: float = self.speed * self.app.delta_time

        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
