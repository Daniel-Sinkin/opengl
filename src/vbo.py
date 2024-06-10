from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable, Optional, TypeAlias, cast

import numpy as np
import pywavefront
from moderngl import Buffer, Context, Program

from util.vertex_data_generator import generate_CubeVBO

if TYPE_CHECKING:
    from graphics_engine import GraphicsEngine

Vertex: TypeAlias = tuple[float, float, float]
VertexIdx: TypeAlias = tuple[int, int, int]


class VBOHandler:
    def __init__(self, ctx: Context):
        self.vbo_map: dict[str, VertexBufferObject] = {
            "cube": CubeVBO(ctx),
            "cat": CatVBO(ctx),
            "skybox": SkyBoxVBO(ctx),
            "advanced_skybox": AdvancedSkyBoxVBO(ctx),
        }

    def destroy(self):
        for vbo in self.vbo_map.values():
            vbo.destroy()


class VertexBufferObject(ABC):
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.vbo: Buffer = self.get_vbo()

    @abstractmethod
    def get_vertex_data(self) -> Iterable[Vertex]: ...

    @property
    @abstractmethod
    def buffer_format(self) -> str: ...

    @property
    @abstractmethod
    def attributes(self) -> list[str]: ...

    def get_vbo(self) -> Buffer:
        vertex_data: Iterable[Vertex] = self.get_vertex_data()
        return self.ctx.buffer(vertex_data)

    def destroy(self) -> None:
        self.vbo.release()


class CubeVBO(VertexBufferObject):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    @property
    def buffer_format(self) -> str:
        return "2f 3f 3f"

    @property
    def attributes(self) -> list[str]:
        return ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self) -> np.ndarray:
        try:
            return cast(np.ndarray, np.load("objects/CubeVBO.npy"))
        except FileNotFoundError:
            print(
                "objects/CubeVBO.npy' was not found, running 'util/vertex_data_generator.py' first."
            )
            generate_CubeVBO()
            try:
                return cast(np.ndarray, np.load("objects/CubeVBO.npy"))
            except FileNotFoundError:
                raise RuntimeError(
                    "objects/CubeVBO.npy' was not found despite running 'util/vertex_data_generator.py'!"
                )


class SkyBoxVBO(VertexBufferObject):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    @property
    def buffer_format(self) -> str:
        return "3f"

    @property
    def attributes(self) -> list[str]:
        return ["in_position"]

    @staticmethod
    def get_data(
        vertices: Iterable[Vertex], indices: Iterable[VertexIdx]
    ) -> np.ndarray[np.float32]:
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float32)

    def get_vertex_data(self) -> np.ndarray:
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]

        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order="C")
        return vertex_data


class AdvancedSkyBoxVBO(VertexBufferObject):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    @property
    def buffer_format(self) -> str:
        return "3f"

    @property
    def attributes(self) -> list[str]:
        return ["in_position"]

    def get_vertex_data(self) -> np.ndarray:
        z = 1 - 1e-4
        vertices = [
            (-1, -1, z),
            (3, -1, z),
            (-1, 3, z),
        ]
        vertex_data = np.array(vertices, dtype=np.float32)
        return vertex_data


class CatVBO(VertexBufferObject):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    @property
    def buffer_format(self) -> str:
        return "2f 3f 3f"

    @property
    def attributes(self) -> list[str]:
        return ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self) -> Iterable[tuple[float, float, float]]:
        objs = pywavefront.Wavefront(
            "objects/cat/20430_Cat_v1_NEW.obj", cache=True, parse=True
        )
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data
