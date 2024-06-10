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

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
            (3, 1, 2),
            (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6,
        ]
        normals = np.array(normals, dtype="f4").reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
