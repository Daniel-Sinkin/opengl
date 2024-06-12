from dataclasses import dataclass
from enum import IntEnum, StrEnum, auto
from typing import Callable, NotRequired, TypeAlias, TypedDict

import glm
import pygame.constants
from glm import vec1, vec2, vec3, vec4

###
# TypeDefs
###
POSITION2D: TypeAlias = tuple[float, float]
POSITION3D: TypeAlias = tuple[float, float, float]
VERTEX_POSITION = POSITION2D | POSITION3D
VERTEX_IDX: TypeAlias = tuple[int, int, int]
VEC_N: TypeAlias = vec1 | vec2 | vec3 | vec4


###
# Constant Variables
###
# fmt: off
# Have to create new objects otherwise we only pass around references
vec3_1 : Callable[[], vec3] = lambda x = 1.0: vec3(x, x, x)
vec3_x : Callable[[], vec3] = lambda x = 1.0: vec3(x, 0.0, 0.0)
vec3_y : Callable[[], vec3] = lambda x = 1.0: vec3(0.0, x, 0.0)
vec3_z : Callable[[], vec3] = lambda x = 1.0: vec3(0.0, 0.0, x)
vec3_xy: Callable[[], vec3] = lambda x = 1.0: vec3(x, x, 0.0)
vec3_xz: Callable[[], vec3] = lambda x = 1.0: vec3(x, 0.0, x)
vec3_yz: Callable[[], vec3] = lambda x = 1.0: vec3(0.0, x, x)
# fmt: on
VEC3_AXIS_PERMUTATIONS: Callable[[], list[vec3]] = lambda: [
    vec3(),
    vec3_1(),
    vec3_x(),
    vec3_y(),
    vec3_z(),
    vec3_xy(),
    vec3_xz(),
    vec3_yz(),
]

MS_TO_SECOND = 1e-4
SECOND_TO_MS = 1000

EPS = 1e-4


###
# Strings
###
@dataclass
class DevStrings:
    UNSUPPORTED_OBJECT_SERIALIZATION_TYPE: Callable[[type], str] = (
        lambda type_: "Unsupported object serialization type %s." % type_
    )


RECORDING_TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"


@dataclass
class VBO:
    IN_TEXCOORD_N = lambda n: f"in_texcoord_{n}"
    IN_TEXCOORD_0 = IN_TEXCOORD_N(0)
    IN_NORMAL = "in_normal"
    IN_POSITION = "in_position"
    IN_COLOR = "in_color"

    FILE_CUBE = "CubeVBO.npy"
    FILE_CYLINDER = "CylinderVBO.npy"
    FILE_SPHERE = "SphereVBO.npy"


###
# Enums
###
class PLAYER_CONTROLLER_MODE(IntEnum):
    FLOATING_CAMERA = auto()
    MENU = auto()
    FPS = auto()


###
# Dicts
###
class CameraSerializeBase(TypedDict):
    position: POSITION3D
    pitch: float
    yaw: float


class CameraSerialize(CameraSerializeBase):
    near_plane: float
    far_plane: float
    speed: float
    sensitivity: float


class BasemodelSerialize(TypedDict):
    vao_name: str
    texture_id: int
    pos: POSITION3D
    rot: POSITION3D
    scale: POSITION3D


class ModelSerialize(BasemodelSerialize):
    rot_update: POSITION3D


SCENE_SERIALIZE_DICT: TypeAlias = dict[int, BasemodelSerialize]
