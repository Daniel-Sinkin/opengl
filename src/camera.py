import typing

import glm
import pygame as pg

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine

FOV = 60
NEAR = 0.1
FAR = 150.0
SPEED = 0.01
SENSITIVITY = 0.05


class Camera:
    def __init__(
        self, app: "GraphicsEngine", position=(0, 0, 4), yaw=-90.0, pitch=16.0
    ):
        self.app: "GraphicsEngine" = app
        self.aspect_ratio: float = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.initial_position = position
        self.position = glm.vec3(position)

        print(id(self.initial_position), id(self.position))

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.initial_yaw, self.initial_pitch = yaw, pitch
        self.yaw, self.pitch = yaw, pitch

        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def rotate(self, rel_x, rel_y) -> None:
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY

        self.pitch = glm.clamp(self.pitch, -89, 89)

    def update_camera_vectors(self) -> None:
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self) -> None:
        self.move()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    # TODO: Move this into the event handler of the renderer
    def move(self) -> None:
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.position = glm.vec3(self.initial_position)
            self.yaw, self.pitch = self.initial_yaw, self.initial_pitch
            return

        velocity = SPEED * self.app.delta_time

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

    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
