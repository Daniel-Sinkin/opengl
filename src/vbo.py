import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable, Optional, TypeAlias, cast

import numpy as np
import pywavefront
import pywavefront.material
from freetype import Face
from moderngl import Buffer, Context, Program

from . import my_logger
from .constants import *
from .settings import Folders
from .vertex_data_generator import (
    generate_CubeVertices,
    generate_CylinderVertices,
    generate_SphereVertices,
)

if TYPE_CHECKING:
    from graphics_engine import GraphicsEngine

logger = my_logger.setup("VBO")

# Don't care about the retvals of the functions as we read from drive
FILENAME_TO_GENERATOR_FUNC_MAP: dict[str, Callable[[], any]] = {
    VBO.FILE_CUBE: generate_CubeVertices,
    VBO.FILE_CYLINDER: generate_CylinderVertices,
    VBO.FILE_SPHERE: generate_SphereVertices,
}


class VBOHandler:
    def __init__(self, ctx: Context):
        self.vbo_map: dict[str, VertexBufferObject] = {
            "cube": Cube(ctx),
            "cat": Cat(ctx),
            "skybox": NaiveSkyBox(ctx),
            "advanced_skybox": SkyBox(ctx),
            "quad": Quad(ctx),
            "sphere": Sphere(ctx),
            "cylinder": Cylinder(ctx),
            "coordinate_axis": Coordinate_Axis(ctx),
            "ui_text": UI_text(ctx),
            "ray": Ray(ctx),
        }

    def destroy(self):
        for vbo in self.vbo_map.values():
            vbo.destroy()


class VertexBufferObject(ABC):
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.vbo: Buffer = self.get_vbo()

    @abstractmethod
    def get_vertex_data(self) -> np.ndarray: ...

    @property
    @abstractmethod
    def buffer_format(self) -> str: ...

    @property
    @abstractmethod
    def attributes(self) -> list[str]: ...

    def get_vbo(self) -> Buffer:
        vertex_data: Iterable[VERTEX_POSITION] = self.get_vertex_data()
        return self.ctx.buffer(vertex_data)

    def destroy(self) -> None:
        self.vbo.release()


class VBOFromFile(VertexBufferObject):
    def __init__(self, ctx: Context, filename: str):
        if "." not in filename:
            logger.warning(
                f"Adding '.npy' to the end of VBO file {filename=}, please fix the function call."
            )
            filename = filename + ".npy"
        elif not filename.endswith(".npy"):
            raise NotImplementedError(
                "Only npy files supported for now. '.obj' files coming soon."
            )

        self.filename: str = filename
        self.filepath: str = os.path.join(Folders.OBJECTS, self.filename)

        super().__init__(ctx)

    def get_vertex_data(self) -> np.ndarray:
        if not os.path.exists(self.filepath):
            logger.warning(f"{self.filepath=} does not exist! Trying to create it now.")
            FILENAME_TO_GENERATOR_FUNC_MAP[self.filename]()
            if not os.path.exists(self.filepath):
                raise RuntimeError(
                    f"{self.filepath=} does not exist despite calling the generation function."
                )

        return cast(np.ndarray, np.load(os.path.join(Folders.OBJECTS, self.filename)))


class Cube(VBOFromFile):
    def __init__(self, ctx: Context):
        super().__init__(ctx, VBO.FILE_CUBE)

    @property
    def buffer_format(self) -> str:
        return "2f 3f 3f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_TEXCOORD_0, VBO.IN_NORMAL, VBO.IN_POSITION]


class Sphere(VBOFromFile):
    def __init__(self, ctx: Context):
        super().__init__(ctx, VBO.FILE_SPHERE)

    @property
    def buffer_format(self) -> str:
        return "3f 3f 2f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_NORMAL, VBO.IN_POSITION, VBO.IN_TEXCOORD_0]


class Cylinder(VBOFromFile):
    def __init__(self, ctx: Context):
        super().__init__(ctx, VBO.FILE_CYLINDER)

    @property
    def buffer_format(self) -> str:
        return "3f 3f 2f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_NORMAL, VBO.IN_POSITION, VBO.IN_TEXCOORD_0]


class NaiveSkyBox(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "3f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_POSITION]

    @staticmethod
    def get_data(
        vertices: Iterable[POSITION3D], indices: Iterable[VERTEX_IDX]
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


class SkyBox(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "3f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_POSITION]

    def get_vertex_data(self) -> np.ndarray:
        z = 1 - 1e-4
        vertices = [
            (-1, -1, z),
            (3, -1, z),
            (-1, 3, z),
        ]
        vertex_data = np.array(vertices, dtype=np.float32)
        return vertex_data


class Cat(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "2f 3f 3f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_TEXCOORD_0, VBO.IN_NORMAL, VBO.IN_POSITION]

    def get_vertex_data(self) -> Iterable[tuple[float, float, float]]:
        objs = pywavefront.Wavefront(
            "objects/cat/20430_Cat_v1_NEW.obj", cache=True, parse=True
        )
        assert len(objs.materials) == 1
        obj: pywavefront.material.Material = objs.materials.popitem()[1]

        vertex_data: tuple[float, ...] = obj.vertices
        assert isinstance(vertex_data, tuple)
        assert all(isinstance(x, float) for x in vertex_data)
        assert len(vertex_data) == 4740096

        return np.array(vertex_data, dtype=np.float32)


class Quad(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "2f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_POSITION]

    # fmt: off
    def get_vertex_data(self) -> np.ndarray:
        return np.array(
            [
                0.85, 0.85,
                  1.0, 0.85,
                 0.85,  1.0,
                  1.0,  1.0,
            ],
            dtype=np.float32,
        )
    # fmt: on


class Coordinate_Axis(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "3f 3f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_POSITION, VBO.IN_COLOR]

    # fmt: off
    def get_vertex_data(self) -> np.ndarray:
        return np.array([
            # Objects         Colors
            0.0,  0.0, 0.0,   1.0, 0.0, 0.0, # X Axis
            1.0,  0.0, 0.0,   1.0, 0.0, 0.0, # RED
            0.0,  0.0, 0.0,   0.0, 1.0, 0.0, # Y Axis
            0.0,  1.0, 0.0,   0.0, 1.0, 0.0, # GREEN
            0.0,  0.0, 0.0,   0.0, 0.0, 1.0, # Z Axis
            0.0,  0.0, 1.0,   0.0, 0.0, 1.0, # BLUE
        ], dtype=np.float32)
    # fmt: on


class Ray(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "3f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_POSITION]

    # fmt: off
    def get_vertex_data(self) -> np.ndarray:
        return np.array([
            0.0,  0.0, 0.0,
            1.0,  0.0, 0.0,
        ], dtype=np.float32)
    # fmt: on


class UI_text(VertexBufferObject):
    @property
    def buffer_format(self) -> str:
        return "4f 2f"

    @property
    def attributes(self) -> list[str]:
        return [VBO.IN_POSITION, VBO.IN_TEXCOORD_0]

    def load_char_texture(self, character):
        self.font_face = Face("/System/Library/Fonts/Supplemental/Arial.ttf")
        self.font_face.set_char_size(48 * 64)

        self.font_face.load_char(character)
        bitmap = self.font_face.glyph.bitmap
        width, height = bitmap.width, bitmap.rows
        texture_data = np.array(bitmap.buffer, dtype=np.ubyte).reshape(height, width)
        return width, height, texture_data

    # fmt: off
    def get_vertex_data(self) -> np.ndarray:
        x = 0
        width, height, texture_data = self.load_char_texture("A")
        xpos, ypos = x, 0
        w, h = int(width), int(height)
        return np.array([
                xpos    , ypos + h, 0.0, 1.0, 0.0,
                xpos    , ypos    , 0.0, 0.0, 0.0,
                xpos + w, ypos    , 0.0, 0.0, 1.0,

                xpos    , ypos + h, 0.0, 1.0, 0.0,
                xpos + w, ypos    , 0.0, 0.0, 1.0,
                xpos + w, ypos + h, 0.0, 1.0, 1.0
            ], dtype='f4')
    # fmt: on
