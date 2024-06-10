import typing
from abc import ABC, abstractmethod

import glm
import moderngl as mgl
import numpy as np
import pygame as pg
from glm import mat3, mat4, vec3

from camera import Camera
from src.constants import *

if typing.TYPE_CHECKING:
    from main import GraphicsEngine


class Model:
    def __init__(
        self,
        app: "GraphicsEngine",
        vao_name: str,
        texture_id: int | str,
        pos: vec3 = vec3_0,
        rot: vec3 = vec3_0,
        scale: vec3 = vec3_1,
    ):
        self.app: "GraphicsEngine" = app
        self.pos: vec3 = pos
        self.rot: vec3 = rot
        self.scale: vec3 = scale
        self.m_model: mat4 = self.get_model_matrix()
        self.texture_id: int | str = texture_id
        self.vao: mgl.VertexArray = app.mesh.vao.vao_map[vao_name]
        self.program: mgl.Program = self.vao.program
        self.camera: Camera = self.app.camera

    @abstractmethod
    def update(self) -> None: ...

    def get_model_matrix(self) -> mat4:
        m_model = glm.mat4()

        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rot.x, vec3_x)
        m_model = glm.rotate(m_model, self.rot.y, vec3_y)
        m_model = glm.rotate(m_model, self.rot.z, vec3_z)

        m_model = glm.scale(m_model, self.scale)

        return m_model

    def render(self) -> None:
        self.update()
        self.vao.render()


class SkyBox(Model):
    def __init__(self, app: "GraphicsEngine"):
        super().__init__(app, "skybox", "skybox")
        self.on_init()

    def update(self):
        self.program["m_view"].write(mat4(mat3(self.camera.m_view)))

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)

        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(mat4(mat3(self.camera.m_view)))


class AdvancedSkyBox(Model):
    def __init__(self, app: "GraphicsEngine"):
        super().__init__(app, "advanced_skybox", "skybox")
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program["m_invProjView"].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)


class ExtendedModel(Model):
    def __init__(
        self,
        app: "GraphicsEngine",
        vao_name: str,
        texture_id,
        pos: vec3 = vec3_0,
        rot: vec3 = vec3_0,
        scale: vec3 = vec3_1,
    ):
        super().__init__(
            app, vao_name=vao_name, texture_id=texture_id, pos=pos, rot=rot, scale=scale
        )
        self.on_init()

    def update(self) -> None:
        self.texture.use()
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    # Why not just put this into the __init__ constructor?
    def on_init(self) -> None:
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_0"] = 0
        self.texture.use()

        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float32)

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo


class Cube(ExtendedModel):
    def __init__(
        self,
        app: "GraphicsEngine",
        tex_id: str | int = 0,
        pos=vec3_0,
        rot=vec3_0,
        scale=vec3_1,
    ):
        super().__init__(app, "cube", tex_id, pos, rot, scale)


class Cat(ExtendedModel):
    def __init__(
        self,
        app: "GraphicsEngine",
        pos: vec3 = vec3_0,
        rot: vec3 = vec3_0,
        scale: vec3 = vec3_1,
        rot_update: vec3 = vec3_0,
    ):
        if rot_update == vec3(0.0, 0.0, 0.0):
            self.rot_update = None
        else:
            self.rot_update = rot_update
        rot_: vec3 = rot - float(np.pi / 2) * vec3_x
        super().__init__(
            app, vao_name="cat", texture_id="cat", pos=pos, rot=rot_, scale=scale
        )

    def update(self):
        if self.rot_update is not None:
            self.m_model = glm.rotate(
                self.m_model, self.rot_update.x * self.app.delta_time, vec3_x
            )
            self.m_model = glm.rotate(
                self.m_model, self.rot_update.y * self.app.delta_time, vec3_y
            )
            self.m_model = glm.rotate(
                self.m_model, self.rot_update.z * self.app.delta_time, vec3_z
            )
        super().update()
