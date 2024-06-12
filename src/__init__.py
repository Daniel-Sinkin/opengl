"""
This contains all project-wide global variables and should be wildcard important by everything.

TODO: Add a `__all__` list to have more finegrained control over what is being imported, but if you
      do write a github action hook that automatically generates it, the overhead of manually adding
      it would absolutely not be worth it.
"""

import datetime as dt
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, StrEnum, auto
from logging import Logger
from typing import (
    TYPE_CHECKING,
    Callable,
    Iterable,
    NotRequired,
    Optional,
    TypeAlias,
    TypedDict,
    TypeVar,
    cast,
    overload,
)

# Suppresses pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import freetype
import glm
import moderngl as mgl
import numpy as np
import pygame as pg
import pygame.constants
import ujson as json
from glm import mat3, mat4, vec1, vec2, vec3, vec4
from moderngl import (
    Buffer,
    Context,
    Framebuffer,
    Program,
    Texture,
    TextureCube,
    VertexArray,
)
from PIL import Image

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
vec2_1  : Callable[[], vec2] = lambda val = 1.0: vec2(val, val)
vec2_x  : Callable[[], vec2] = lambda val = 1.0: vec2(val, 0.0)
vec2_y  : Callable[[], vec2] = lambda val = 1.0: vec2(0.0, val)

vec3_1  : Callable[[], vec3] = lambda val = 1.0: vec3(val, val, val)
vec3_x  : Callable[[], vec3] = lambda val = 1.0: vec3(val, 0.0, 0.0)
vec3_y  : Callable[[], vec3] = lambda val = 1.0: vec3(0.0, val, 0.0)
vec3_z  : Callable[[], vec3] = lambda val = 1.0: vec3(0.0, 0.0, val)
vec3_xy : Callable[[], vec3] = lambda val = 1.0: vec3(val, val, 0.0)
vec3_xz : Callable[[], vec3] = lambda val = 1.0: vec3(val, 0.0, val)
vec3_yz : Callable[[], vec3] = lambda val = 1.0: vec3(0.0, val, val)

vec4_1  : Callable[[], vec4] = lambda val = 1.0: vec4(val, val, val, val)
vec4_x  : Callable[[], vec4] = lambda val = 1.0: vec4(val, 0.0, 0.0, 0.0)
vec4_y  : Callable[[], vec4] = lambda val = 1.0: vec4(0.0, val, 0.0, 0.0)
vec4_z  : Callable[[], vec4] = lambda val = 1.0: vec4(0.0, 0.0, val, 0.0)
vec4_w  : Callable[[], vec4] = lambda val = 1.0: vec4(0.0, 0.0, 0.0, val)
vec4_xy : Callable[[], vec4] = lambda val = 1.0: vec4(val, val, 0.0, 0.0)
vec4_xz : Callable[[], vec4] = lambda val = 1.0: vec4(val, 0.0, val, 0.0)
vec4_xw : Callable[[], vec4] = lambda val = 1.0: vec4(val, 0.0, 0.0, val)
vec4_yz : Callable[[], vec4] = lambda val = 1.0: vec4(0.0, val, val, 0.0)
vec4_yw : Callable[[], vec4] = lambda val = 1.0: vec4(0.0, val, 0.0, val)
vec4_zw : Callable[[], vec4] = lambda val = 1.0: vec4(0.0, 0.0, val, val)
vec4_xyz: Callable[[], vec4] = lambda val = 1.0: vec4(val, val, val, 0.0)
vec4_xyw: Callable[[], vec4] = lambda val = 1.0: vec4(val, val, 0.0, val)
vec4_xzw: Callable[[], vec4] = lambda val = 1.0: vec4(val, 0.0, val, val)
vec4_yzw: Callable[[], vec4] = lambda val = 1.0: vec4(0.0, val, val, val)

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


@dataclass
class DevStrings:
    UNSUPPORTED_OBJECT_SERIALIZATION_TYPE: Callable[[type], str] = (
        lambda type_: "Unsupported object serialization type '%s'." % type_
    )
