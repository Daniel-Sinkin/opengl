from abc import ABC, abstractmethod
from typing import Iterable, Optional, TypeAlias

import numpy as np
from moderngl import Buffer, Context, Program

Vertex: TypeAlias = tuple[float, float, float]
VertexIdx: TypeAlias = tuple[int, int, int]


class VBOHandler:
    def __init__(self, ctx: Context):
        self.vbo_map: dict[str, VertexBufferObject] = {"cube": CubeVBO(ctx)}

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

    @staticmethod
    def get_data(
        vertices: Iterable[Vertex], indices: Iterable[VertexIdx]
    ) -> np.ndarray[np.float32]:
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float32)

    def get_vertex_data(self):
        try:
            return np.load("objects/CubeVBO.npy")
        except FileNotFoundError:
            print(
                "objects/CubeVBO.npy' was not found, run 'util/vertex_data_generator.py' first."
            )
