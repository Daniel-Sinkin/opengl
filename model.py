import typing
from abc import ABC, abstractmethod

import glm
import moderngl as mgl
import numpy as np
import pygame as pg

from camera import Camera

if typing.TYPE_CHECKING:
    from main import GraphicsEngine


class Model:
    def __init__(self, app: "GraphicsEngine", vao_name: str, texture_id: int):
        self.app: GraphicsEngine = app
        self.m_model: glm.mat4x4 = self.get_model_matrix()
        self.texture_id: int = texture_id
        self.vao: mgl.VertexArray = app.mesh.vao.vao_map[vao_name]
        self.program: mgl.Program = self.vao.program
        self.camera: Camera = self.app.camera

    @abstractmethod
    def update(self) -> None: ...

    def get_model_matrix(self) -> glm.mat4x4:
        return glm.mat4()

    def render(self) -> None:
        self.update()
        self.vao.render()


class Cube(Model):
    def __init__(self, app: "GraphicsEngine"):
        super().__init__(app, vao_name="cube", texture_id=0)
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

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program
