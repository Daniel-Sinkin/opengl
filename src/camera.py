import typing

import glm
import pygame as pg
from glm import mat4

from .constants import *
from .settings import Settings_Camera

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine


class Camera:
    def __init__(
        self,
        app: "GraphicsEngine",
        position: POINT = None,
        yaw=Settings_Camera.INITIAL_YAW,
        pitch=Settings_Camera.INITAL_PITCH,
    ):
        self.app: GraphicsEngine = app
        self.aspect_ratio: float = app.window_size[0] / app.window_size[1]

        if position is not None:
            self.initial_position: POINT = position
        else:
            self.initial_position: POINT = Settings_Camera.INITIAL_POSITION

        self.position = vec3(*self.initial_position)

        self.original_fov = Settings_Camera.FOV
        self.fov = self.original_fov

        self.near_plane: float = Settings_Camera.NEAR
        self.far_plane: float = Settings_Camera.FAR
        self.speed: float = Settings_Camera.SPEED
        self.sensitivity: float = Settings_Camera.SENSITIVITY

        self.up: vec3 = vec3_y
        self.right: vec3 = vec3_x
        self.forward: vec3 = -vec3_z

        self.initial_yaw, self.initial_pitch = yaw, pitch
        self.yaw, self.pitch = yaw, pitch

        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def rotate(self, rel_x, rel_y) -> None:
        self.yaw += rel_x * self.sensitivity
        self.pitch -= rel_y * self.sensitivity

        self.pitch = glm.clamp(self.pitch, *Settings_Camera.PITCH_BOUNDS)

    def update_camera_vectors(self) -> None:
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self) -> None:
        self.update_camera_vectors()
        if self.app.camera_projection_has_changed:
            self.m_proj = self.get_projection_matrix()
        self.m_view: mat4 = self.get_view_matrix()

    # TODO: Move this into the event handler of the renderer
    def move(self) -> None:
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.position = glm.vec3(self.initial_position)
            self.yaw, self.pitch = self.initial_yaw, self.initial_pitch
            return

        velocity: float = self.speed * self.app.delta_time

        if keys[pg.K_LSHIFT]:
            velocity *= 3

        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_UP]:
            self.position += self.up * velocity
        if keys[pg.K_DOWN]:
            self.position -= self.up * velocity

    def get_view_matrix(self) -> mat4:
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self) -> mat4:
        return glm.perspective(
            glm.radians(self.fov),
            self.aspect_ratio,
            self.near_plane,
            self.far_plane,
        )

    def reset(self) -> None:
        self.position = vec3(self.initial_position)
        self.yaw, self.pitch = (
            self.initial_yaw,
            self.initial_pitch,
        )
        self.fov = self.original_fov
        self.camera_projection_has_changed = True

    def adjust_fov(self, amount: float) -> None:
        new_fov = glm.clamp(self.fov + amount, *Settings_Camera.FOV_BOUNDS)
        if new_fov != self.fov:
            self.camera_projection_has_changed = True
            self.camera.fov = new_fov
