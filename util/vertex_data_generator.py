import os
from typing import Iterable, TypeAlias

import numpy as np

Vertex: TypeAlias = tuple[float, float, float]
VertexIdx: TypeAlias = tuple[int, int, int]


def vertex_idx_transform(
    vertices: Iterable[Vertex], indices: Iterable[VertexIdx]
) -> np.ndarray[np.float32]:
    data = [vertices[ind] for triangle in indices for ind in triangle]
    return np.array(data, dtype=np.float32)


def generate_CubeVBO(folderpath="VertexData", filename="CubeVBO.npy") -> None:
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
    vertex_data = vertex_idx_transform(vertices, indices)

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
    tex_coord_data = vertex_idx_transform(tex_coord_vertices, tex_coord_indices)

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

    np.save(os.path.join(folderpath, filename), vertex_data)


if __name__ == "__main__":
    generate_CubeVBO()
