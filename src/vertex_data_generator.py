import os
from typing import Iterable, TypeAlias

import numpy as np

from .constants import VBO
from .settings import Folders


# TODO: Either remove this by inlining the functionality, solve it in another way or make this func
#       more general, only using it for one construction feels weird.
# TODO: Improve the type hinting
def vertex_idx_transform(
    vertices: list[tuple[float, float, float]], indices: list[tuple[int, int, int]]
) -> np.ndarray[np.float32]:
    data = [vertices[ind] for triangle in indices for ind in triangle]
    return np.array(data, dtype=np.float32)


# TODO: Rewrite this, this is from a tutorial I watched when starting out and I don't like the
#       approach that was taken.
# TODO: Improve the type hinting
def generate_CubeVertices(folderpath=Folders.OBJECTS, filename=VBO.FILE_CUBE) -> None:
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


# TODO: Improve the type hinting
def generate_SphereVertices(
    folderpath=Folders.OBJECTS,
    filename=VBO.FILE_SPHERE,
    radius: float = 1.0,
    sectors: int = 36,
    stacks: int = 18,
) -> np.ndarray[np.float32]:
    vertices = []
    normals = []
    tex_coords = []
    indices = []

    for i in range(stacks + 1):
        stack_angle = np.pi / 2 - i * np.pi / stacks  # from pi/2 to -pi/2
        xy = radius * np.cos(stack_angle)  # r * cos(u)
        z = radius * np.sin(stack_angle)  # r * sin(u)

        for j in range(sectors + 1):
            sector_angle = j * 2 * np.pi / sectors  # from 0 to 2pi

            x = xy * np.cos(sector_angle)  # r * cos(u) * cos(v)
            y = xy * np.sin(sector_angle)  # r * cos(u) * sin(v)
            vertices.append((x, y, z))

            nx = x / radius
            ny = y / radius
            nz = z / radius
            normals.append((nx, ny, nz))

            s = j / sectors
            t = i / stacks
            tex_coords.append((s, t))

    for i in range(stacks):
        for j in range(sectors):
            first = i * (sectors + 1) + j
            second = first + sectors + 1

            indices.append((first, second, first + 1))
            indices.append((second, second + 1, first + 1))

    vertices = np.array(vertices, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    tex_coords = np.array(tex_coords, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    def vertex_idx_transform(vertices, normals, tex_coords, indices):
        transformed_data = []
        for triangle in indices:
            for ind in triangle:
                transformed_data.extend(normals[ind])
                transformed_data.extend(vertices[ind])
                transformed_data.extend(tex_coords[ind])
        return np.array(transformed_data, dtype=np.float32)

    vertex_data = vertex_idx_transform(vertices, normals, tex_coords, indices)

    np.save(os.path.join(folderpath, filename), vertex_data)
    return vertex_data


# TODO: Improve the type hinting
def generate_CylinderVertices(
    folderpath=Folders.OBJECTS,
    filename=VBO.FILE_CYLINDER,
    radius: float = 1.0,
    height: float = 2.0,
    sectors: int = 36,
) -> np.ndarray[np.float32]:
    vertices = []
    normals = []
    tex_coords = []
    indices = []

    half_height = height / 2

    # Vertices for the top and bottom circles
    for i in range(sectors + 1):
        sector_angle = i * 2 * np.pi / sectors

        x = radius * np.cos(sector_angle)
        y = radius * np.sin(sector_angle)

        # Top circle
        vertices.append((x, y, half_height))
        normals.append((0, 0, 1))
        tex_coords.append((i / sectors, 1))

        # Bottom circle
        vertices.append((x, y, -half_height))
        normals.append((0, 0, -1))
        tex_coords.append((i / sectors, 0))

    # Vertices for the sides
    for i in range(sectors + 1):
        sector_angle = i * 2 * np.pi / sectors

        x = radius * np.cos(sector_angle)
        y = radius * np.sin(sector_angle)

        # Top edge of the side
        vertices.append((x, y, half_height))
        normals.append((x / radius, y / radius, 0))
        tex_coords.append((i / sectors, 1))

        # Bottom edge of the side
        vertices.append((x, y, -half_height))
        normals.append((x / radius, y / radius, 0))
        tex_coords.append((i / sectors, 0))

    # Indices for the top and bottom circles
    top_center_index = len(vertices)
    bottom_center_index = len(vertices) + 1
    vertices.append((0, 0, half_height))  # Top center
    normals.append((0, 0, 1))
    tex_coords.append((0.5, 0.5))
    vertices.append((0, 0, -half_height))  # Bottom center
    normals.append((0, 0, -1))
    tex_coords.append((0.5, 0.5))

    for i in range(sectors):
        next_i = (i + 1) % sectors
        top_vertex = 2 * i
        next_top_vertex = 2 * next_i
        bottom_vertex = 2 * i + 1
        next_bottom_vertex = 2 * next_i + 1

        # Top circle
        indices.append((top_center_index, top_vertex, next_top_vertex))

        # Bottom circle
        indices.append((bottom_center_index, next_bottom_vertex, bottom_vertex))

    # Indices for the side surface
    side_offset = 2 * (sectors + 1)
    for i in range(sectors):
        top_edge = side_offset + 2 * i
        next_top_edge = side_offset + 2 * ((i + 1) % sectors)
        bottom_edge = top_edge + 1
        next_bottom_edge = next_top_edge + 1

        indices.append((top_edge, bottom_edge, next_top_edge))
        indices.append((bottom_edge, next_bottom_edge, next_top_edge))

    vertices = np.array(vertices, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    tex_coords = np.array(tex_coords, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    def vertex_idx_transform(vertices, normals, tex_coords, indices):
        transformed_data = []
        for triangle in indices:
            for ind in triangle:
                transformed_data.extend(normals[ind])
                transformed_data.extend(vertices[ind])
                transformed_data.extend(tex_coords[ind])
        return np.array(transformed_data, dtype=np.float32)

    vertex_data = vertex_idx_transform(vertices, normals, tex_coords, indices)

    np.save(os.path.join(folderpath, filename), vertex_data)
    return vertex_data


if __name__ == "__main__":
    generate_SphereVertices()
    generate_CubeVertices()
    generate_CylinderVertices()
