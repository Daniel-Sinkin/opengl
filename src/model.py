import typing
from abc import ABC, abstractmethod
from typing import Optional

import glm
import moderngl as mgl
import numpy as np
import pygame as pg
import ujson as json
from glm import mat3, mat4, vec2, vec3
from moderngl import Program

from .camera import Camera
from .constants import *

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine


class Line:
    def __init__(self, app: "GraphicsEngine"):
        self.app: GraphicsEngine = app
        self.camera: Camera = self.app.camera
        self.vao_name = "line"
        self.vao: mgl.VertexArray = app.mesh.vao.vao_map[self.vao_name]

        self.program: Program = self.vao.program

    def update(self) -> None:
        mvp = self.camera.m_proj * self.camera.m_view
        self.program["mvp"].write(mvp)

    def render(self) -> None:
        self.update()
        self.vao.render(mgl.LINES)


class Quad:
    def __init__(self, app: "GraphicsEngine"):
        self.app: GraphicsEngine = app
        self.vao_name = "quad"
        self.vao: mgl.VertexArray = app.mesh.vao.vao_map[self.vao_name]

        self.program: Program = self.vao.program

    def update(self) -> None:
        if self.app.menu_open:
            self.program["menuOpen"] = True
        else:
            self.program["menuOpen"] = False

    def render(self) -> None:
        self.vao.render(mgl.TRIANGLE_STRIP)


class BaseModel:
    def __init__(
        self,
        app: "GraphicsEngine",
        vao_name: str,
        texture_id: int | str,
        pos: vec3 = vec3_0(),
        rot: vec3 = vec3_0(),
        scale: vec3 = vec3_1(),
    ):
        self.app: GraphicsEngine = app

        self.pos: vec3 = pos
        self.rot: vec3 = rot
        self.scale: vec3 = scale

        # TODO: Find a good way of copying so we don't have to create it twice
        self.m_model_initial = self.get_initial_model_matrix()
        self.m_model: mat4 = self.get_initial_model_matrix()

        self.texture_id: int | str = texture_id

        self.vao_name = vao_name
        self.vao: mgl.VertexArray = app.mesh.vao.vao_map[vao_name]

        self.program: Program = self.vao.program
        self.camera: Camera = self.app.camera

        self.scene_idx = None

    @abstractmethod
    def update(self) -> None: ...

    def get_initial_model_matrix(self) -> mat4:
        """
        Applies the initial transformations and returns them as a single 4x4 model matrix.
        """
        m_model: mat4 = glm.mat4()

        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rot.x, vec3_x())
        m_model = glm.rotate(m_model, self.rot.y, vec3_y())
        m_model = glm.rotate(m_model, self.rot.z, vec3_z())

        m_model = glm.scale(m_model, self.scale)

        return m_model

    def render(self) -> None:
        self.update()
        self.vao.render()

    def __str__(self) -> None:
        return f"BaseModel({self.vao_name=},{self.texture_id=},{self.pos=},{self.rot=},{self.scale=})"

    def serialize(
        self, serialize_type="json", filepath=None, include_scene_idx=False
    ) -> BASEMODEL_SERIALIZE:
        if serialize_type != "json":
            raise NotImplementedError(
                DevStringsLambda.UNSUPPORTED_OBJECT_SERIALIZATION_TYPE(serialize_type)
            )
        dict_ = BASEMODEL_SERIALIZE(
            vao_name=self.vao_name,
            texture_id=self.texture_id,
            pos=tuple(self.pos),
            rot=tuple(self.rot),
            scale=tuple(self.scale),
        )
        if include_scene_idx:
            if self.scene_idx is None:
                self.app.logger.warn(
                    f"Tried to serialize `scene_idx` of {self}, but it's not set!"
                )
            else:
                dict_["scene_idx"] = self.scene_idx

        if filepath is not None:
            json.dump(dict_, filepath)

        return dict_


class SkyBox(BaseModel):
    def __init__(self, app: "GraphicsEngine"):
        super().__init__(app, "advanced_skybox", "skybox")
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program["m_invProjView"].write(glm.inverse(self.camera.m_proj * m_view))

        if self.app.menu_open:
            self.program["menuOpen"] = True
        else:
            self.program["menuOpen"] = False

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)


class Model(BaseModel):
    """
    This class is a base for all "real" models, things which are in the world, have a shadow
    and interact with the light system.

    The `rot_update` vector gives a rotation that will be continuously applied, should be a
    small value as it'll be updated every frame.
    """

    def __init__(
        self,
        app: "GraphicsEngine",
        vao_name: str,
        texture_id,
        pos: vec3 = vec3_0(),
        rot: vec3 = vec3_0(),
        scale: vec3 = vec3_1(),
        rot_update: Optional[vec3] = None,
    ):
        self.rot_update = rot_update
        self.scale_animation_function = None
        self.previous_scale_factor = vec3_1()

        super().__init__(
            app, vao_name=vao_name, texture_id=texture_id, pos=pos, rot=rot, scale=scale
        )
        self.on_init()

    def __str__(self):
        return (
            super().__str__().replace("BaseModel", "Model")[:-1]
            + f",{self.rot_update=})"
        )

    def serialize(
        self, serialize_type="json", filepath=None, include_scene_idx=False
    ) -> MODEL_SERIALIZE:
        if serialize_type != "json":
            raise NotImplementedError(
                DevStringsLambda.UNSUPPORTED_OBJECT_SERIALIZATION_TYPE(serialize_type)
            )
        dict_: BASEMODEL_SERIALIZE = super().serialize(serialize_type, None, False)
        dict_["rot_update"] = self.rot_update
        if include_scene_idx:
            dict_["scene_idx"] = self.scene_idx

        if filepath is not None:
            json.dump(dict_, filepath)

        return dict_

    def update(self) -> None:
        self.texture.use(location=0)
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

        if self.app.camera_projection_has_changed:
            self.program["m_proj"].write(self.app.camera.m_proj)
            self.shadow_program["m_proj"].write(self.camera.m_proj)

        if self.rot_update is not None:
            self.m_model = glm.rotate(
                self.m_model, self.rot_update.x * self.app.delta_time_s, vec3_x()
            )
            self.m_model = glm.rotate(
                self.m_model, self.rot_update.y * self.app.delta_time_s, vec3_y()
            )
            self.m_model = glm.rotate(
                self.m_model, self.rot_update.z * self.app.delta_time_s, vec3_z()
            )

        if self.scale_animation_function is not None:
            self.m_model = glm.scale(
                self.m_model_initial,
                self.scale_animation_function(self.alpha + self.app.frame_counter / 50),
            )

        if self.app.menu_open:
            self.program["menuOpen"] = True
        else:
            self.program["menuOpen"] = False

    def update_shadow(self):
        self.shadow_program["m_model"].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self) -> None:
        self.program["m_view_light"].write(self.app.light.m_view_light)

        # resolution
        self.program["u_resolution"].write(vec2(self.app.window_size))

        # Depth Texture
        self.depth_texture: mgl.Texture = self.app.mesh.texture.textures[
            "depth_texture"
        ]
        self.program["shadowMap"] = 1
        self.depth_texture.use(location=1)

        # Shadows
        self.shadow_vao: mgl.VertexArray = self.app.mesh.vao.vao_map[
            "shadow_" + self.vao_name
        ]
        self.shadow_program: Program = self.shadow_vao.program
        self.shadow_program["m_proj"].write(self.camera.m_proj)
        self.shadow_program["m_view_light"].write(self.app.light.m_view_light)
        self.shadow_program["m_model"].write(self.m_model)

        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_0"] = 0
        self.texture.use(location=0)

        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.intensity_ambient)
        self.program["light.Id"].write(self.app.light.intensity_diffuse)
        self.program["light.Is"].write(self.app.light.intensity_specular)

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float32)

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo


class Cube(Model):
    def __init__(
        self,
        app: "GraphicsEngine",
        tex_id: str | int = 0,
        pos=vec3_0(),
        rot=vec3_0(),
        scale=vec3_1(),
        rot_update: Optional[vec3] = None,
    ):
        super().__init__(app, "cube", tex_id, pos, rot, scale, rot_update)


class MovingCube(Cube):
    """
    A cube that continually does its initial rotation instead of just once.
    """

    def __init__(
        self,
        app: "GraphicsEngine",
        tex_id: str | int = 0,
        pos=vec3_0(),
        rot=vec3_0(),
        scale=vec3_1(),
    ):
        super().__init__(app, tex_id, pos, rot, scale)

    def update(self):
        self.m_model = glm.rotate(
            self.m_model, self.app.delta_time * self.rot.x, vec3_x()
        )
        self.m_model = glm.rotate(
            self.m_model, self.app.delta_time * self.rot.y, vec3_y()
        )
        self.m_model = glm.rotate(
            self.m_model, self.app.delta_time * self.rot.z, vec3_z()
        )

        super().update()


class Cat(Model):
    """
    Loads the cat model obtained from:
        - https://free3d.com/3d-model/cat-v1--220685.html1
    """

    def __init__(
        self,
        app: "GraphicsEngine",
        pos: vec3 = vec3_0(),
        rot: vec3 = vec3_0(),
        scale: vec3 = vec3_1(),
    ):
        # Model data is rotated weirdly
        rot_: vec3 = rot - float(np.pi / 2) * vec3_x()
        super().__init__(
            app, vao_name="cat", texture_id="cat", pos=pos, rot=rot_, scale=scale
        )


class Sphere(Model):
    def __init__(
        self,
        app: "GraphicsEngine",
        texture_id=0,
        pos: vec3 = vec3_0(),
        rot: vec3 = vec3_0(),
        scale: vec3 = vec3_1(),
    ):
        super().__init__(
            app, vao_name="sphere", texture_id=texture_id, pos=pos, rot=rot, scale=scale
        )
