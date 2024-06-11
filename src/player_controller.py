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
from .settings import Physics

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

        self.camera_offset: vec3 = vec3_y()

        self.forward: vec3 = glm.normalize(
            vec3(self.camera.forward.x, 0, self.camera.forward.z)
        )
        self.right: vec3 = vec3(-self.forward.z, 0, self.forward.x)

        # TODO: Add to settings
        self.speed = 0.01
        self.speed_turbo = 0.018
        self.jump_force = 0.3

        # Direction that physics will push you
        self.force_vector: vec3 = vec3_0()
        # The force with which you move
        self.move_force: vec3 = vec3_0()
        self.jump_force_vector = vec3_0()

        self.is_jumping = False

    @property
    def on_ground(self) -> bool:
        return (self.position.y <= 3.001) and (self.force_vector.y <= 0)

    def update(self) -> None:
        if self.app.player_controller_mode == PLAYER_CONTROLLER_MODE.FPS:
            self.camera.position = self.position + self.camera_offset

            self.forward: vec3 = glm.normalize(
                vec3(self.camera.forward.x, 0, self.camera.forward.z)
            )
            # glm.cross(self.foward, vec3_y()) == (vx, 0, vz) x (0, 1, 0) == (-vz, 0, vx)
            self.right: vec3 = vec3(-self.forward.z, 0, self.forward.x)

        self.fixed_update()

    def move(self) -> None:
        """
        When controlling a floating camera we can just pass through objects so we
        don't need any bound checks.
        """
        keys: ScancodeWrapper = pg.key.get_pressed()

        if keys[pg.K_LSHIFT]:
            velocity: float = self.speed_turbo * self.app.delta_time
        else:
            velocity: float = self.speed * self.app.delta_time

        move_direction = vec3_0()
        needs_normalizing = True
        if keys[pg.K_w]:
            move_direction += self.forward
        elif keys[pg.K_s]:
            move_direction -= self.forward
        else:
            needs_normalizing = False

        if keys[pg.K_a]:
            move_direction -= self.right
        elif keys[pg.K_d]:
            move_direction += self.right
        else:
            needs_normalizing = False

        # Surprisingly this is still faster than dividing sqrt2 even if we cache SQRT2
        if needs_normalizing:
            move_direction = glm.normalize(move_direction)

        if not self.is_jumping:
            self.move_force += move_direction

        if glm.length(self.move_force) > 0.5:
            self.move_force = 0.5 * glm.normalize(self.move_force)

        if keys[pg.K_SPACE] and self.on_ground:
            self.force_vector.y += self.jump_force
            self.jump_force_direction = glm.normalize(self.move_force)
            self.jump_force_vector = self.move_force
            self.move_force = vec3_0()
            self.is_jumping = True

    def fixed_update(self) -> None:
        """
        Deals with all the physics stuff, later the game logic, rendering pipeline and physics
        will be out of sync (for example physics will need more than 1 iteration per frame).
        """
        self.process_physics()

    def process_physics(self) -> None:
        if not self.on_ground:
            self.force_vector.y -= (
                Physics.GRAVITATIONAL_CONSTANT * self.app.delta_time_s
            )

        self.position += self.force_vector + self.move_force + self.jump_force_vector

        move_magnitude_sq = glm.length2(self.move_force)
        if move_magnitude_sq > 0.001:
            self.move_force -= (
                35 * glm.normalize(self.move_force) * self.app.delta_time_s
            )
        else:
            self.move_force = vec3_0()

        self.jump_force_vector -= (
            0.2 * glm.l2Norm(self.jump_force_vector) * self.app.delta_time_s
        )

        if self.on_ground:
            self.position.y = 3
            self.force_vector.y = 0
            self.jump_force_vector = vec3_0()
            self.jump_force_direction = vec3_0()

            self.is_jumping = False
