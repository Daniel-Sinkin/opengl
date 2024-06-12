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
# Have to create new objects otherwise we only pass around references which can then be overwritten
vec2_1  : Callable[[], vec2] = lambda x = 1.0: vec2(  x,   x)
vec2_x  : Callable[[], vec2] = lambda x = 1.0: vec2(  x, 0.0)
vec2_y  : Callable[[], vec2] = lambda x = 1.0: vec2(0.0,   x)

vec3_1  : Callable[[], vec3] = lambda x = 1.0: vec3(  x,   x,   x)
vec3_x  : Callable[[], vec3] = lambda x = 1.0: vec3(  x, 0.0, 0.0)
vec3_y  : Callable[[], vec3] = lambda x = 1.0: vec3(0.0,   x, 0.0)
vec3_z  : Callable[[], vec3] = lambda x = 1.0: vec3(0.0, 0.0,   x)
vec3_xy : Callable[[], vec3] = lambda x = 1.0: vec3(  x,   x, 0.0)
vec3_xz : Callable[[], vec3] = lambda x = 1.0: vec3(  x, 0.0,   x)
vec3_yz : Callable[[], vec3] = lambda x = 1.0: vec3(0.0,   x,   x)

vec4_1  : Callable[[], vec4] = lambda x = 1.0: vec4(  x,   x,   x,   x)
vec4_x  : Callable[[], vec4] = lambda x = 1.0: vec4(  x, 0.0, 0.0, 0.0)
vec4_y  : Callable[[], vec4] = lambda x = 1.0: vec4(0.0,   x, 0.0, 0.0)
vec4_z  : Callable[[], vec4] = lambda x = 1.0: vec4(0.0, 0.0,   x, 0.0)
vec4_w  : Callable[[], vec4] = lambda x = 1.0: vec4(0.0, 0.0, 0.0,   x)
vec4_xy : Callable[[], vec4] = lambda x = 1.0: vec4(  x,   x, 0.0, 0.0)
vec4_xz : Callable[[], vec4] = lambda x = 1.0: vec4(  x, 0.0,   x, 0.0)
vec4_xw : Callable[[], vec4] = lambda x = 1.0: vec4(  x, 0.0, 0.0,   x)
vec4_yz : Callable[[], vec4] = lambda x = 1.0: vec4(0.0,   x,   x, 0.0)
vec4_yw : Callable[[], vec4] = lambda x = 1.0: vec4(0.0,   x, 0.0,   x)
vec4_zw : Callable[[], vec4] = lambda x = 1.0: vec4(0.0, 0.0,   x,   x)
vec4_xyz: Callable[[], vec4] = lambda x = 1.0: vec4(  x,   x,   x, 0.0)
vec4_xyw: Callable[[], vec4] = lambda x = 1.0: vec4(  x,   x, 0.0,   x)
vec4_xzw: Callable[[], vec4] = lambda x = 1.0: vec4(  x, 0.0,   x,   x)
vec4_yzw: Callable[[], vec4] = lambda x = 1.0: vec4(0.0,   x,   x,   x)

VEC2_AXIS_PERMUTATIONS: Callable[[], list[vec2]] = lambda: [
    vec2(),
    vec2_1(),
    vec2_x(),
    vec2_y(),
]
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
VEC4_AXIS_PERMUTATIONS: Callable[[], list[vec4]] = lambda: [
    vec4_1(),
    vec4_x(),
    vec4_y(),
    vec4_z(),
    vec4_w(),
    vec4_xy(),
    vec4_xz(),
    vec4_xw(),
    vec4_yz(),
    vec4_yw(),
    vec4_zw(),
    vec4_xyz(),
    vec4_xyw(),
    vec4_xzw(),
    vec4_yzw(),
]
# fmt: on

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
