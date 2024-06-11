from enum import IntEnum, auto
from typing import Callable, NotRequired, TypeAlias, TypedDict

import pygame.constants
from glm import vec3


###
# Strings
###
class DevStringsLambda:
    UNSUPPORTED_OBJECT_SERIALIZATION_TYPE: Callable[[type], str] = (
        lambda type_: "Unsupported object serialization type %s." % type_
    )


RECORDING_TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"


###
# Enums
###
class PLAYER_CONTROLLER_MODE(IntEnum):
    FLOATING_CAMERA = auto()
    UNLOCKED_MOUSE = auto()
    PLAYER_CONTROLLER_FPS = auto()


###
# Constant Variables
###
vec3_0 = vec3(0.0, 0.0, 0.0)
vec3_1 = vec3(1.0, 1.0, 1.0)
vec3_x = vec3(1.0, 0.0, 0.0)
vec3_y = vec3(0.0, 1.0, 0.0)
vec3_z = vec3(0.0, 0.0, 1.0)
vec3_xy = vec3(1.0, 1.0, 0.0)
vec3_xz = vec3(1.0, 0.0, 1.0)
vec3_yz = vec3(0.0, 1.0, 1.0)

MS_TO_SECOND = 1e-4
SECOND_TO_MS = 1000

###
# TypeDefs
###
POSITION3D: TypeAlias = tuple[float, float, float]
VERTEX_IDX: TypeAlias = tuple[int, int, int]


###
# Dicts
###
class CAMERA_SERIALIZE_BASE(TypedDict):
    position: POSITION3D
    pitch: float
    yaw: float


class CAMERA_SERIALIZE(CAMERA_SERIALIZE_BASE):
    near_plane: float
    far_plane: float
    speed: float
    sensitivity: float


class BASEMODEL_SERIALIZE(TypedDict):
    vao_name: str
    texture_id: int
    pos: POSITION3D
    rot: POSITION3D
    scale: POSITION3D


class MODEL_SERIALIZE(BASEMODEL_SERIALIZE):
    rot_update: POSITION3D


SCENE_SERIALIZE_DICT: TypeAlias = dict[int, BASEMODEL_SERIALIZE]
