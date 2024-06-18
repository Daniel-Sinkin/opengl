"""
This contains all project-wide global variables and should be wildcard important by everything.
"""

import dataclasses
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
    Literal,
    NotRequired,
    Optional,
    Required,
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
# Project Setup
###

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
def vec2_x(val = 1.0) -> vec2: return vec2(val, 0.0)
def vec2_y(val = 1.0) -> vec2: return vec2(0.0, val)

def vec3_x (val = 1.0) -> vec3: return vec3(val, 0.0, 0.0)
def vec3_y (val = 1.0) -> vec3: return vec3(0.0, val, 0.0)
def vec3_z (val = 1.0) -> vec3: return vec3(0.0, 0.0, val)
def vec3_xy(val = 1.0) -> vec3: return vec3(val, val, 0.0)
def vec3_xz(val = 1.0) -> vec3: return vec3(val, 0.0, val)
def vec3_yz(val = 1.0) -> vec3: return vec3(0.0, val, val)

def vec4_x  (val = 1.0) -> vec4: return vec4(val, 0.0, 0.0, 0.0)
def vec4_y  (val = 1.0) -> vec4: return vec4(0.0, val, 0.0, 0.0)
def vec4_z  (val = 1.0) -> vec4: return vec4(0.0, 0.0, val, 0.0)
def vec4_w  (val = 1.0) -> vec4: return vec4(0.0, 0.0, 0.0, val)
def vec4_xy (val = 1.0) -> vec4: return vec4(val, val, 0.0, 0.0)
def vec4_xz (val = 1.0) -> vec4: return vec4(val, 0.0, val, 0.0)
def vec4_xw (val = 1.0) -> vec4: return vec4(val, 0.0, 0.0, val)
def vec4_yz (val = 1.0) -> vec4: return vec4(0.0, val, val, 0.0)
def vec4_yw (val = 1.0) -> vec4: return vec4(0.0, val, 0.0, val)
def vec4_zw (val = 1.0) -> vec4: return vec4(0.0, 0.0, val, val)
def vec4_xyz(val = 1.0) -> vec4: return vec4(val, val, val, 0.0)
def vec4_xyw(val = 1.0) -> vec4: return vec4(val, val, 0.0, val)
def vec4_xzw(val = 1.0) -> vec4: return vec4(val, 0.0, val, val)
def vec4_yzw(val = 1.0) -> vec4: return vec4(0.0, val, val, val)

VEC2_AXIS_PERMUTATIONS: Callable[[], list[vec2]] = lambda: [
    vec2(),
    vec2(1.0),
    vec2_x(),
    vec2_y(),
]
VEC3_AXIS_PERMUTATIONS: Callable[[], list[vec3]] = lambda: [
    vec3(),
    vec3(1.0),
    vec3_x(),
    vec3_y(),
    vec3_z(),
    vec3_xy(),
    vec3_xz(),
    vec3_yz(),
]
VEC4_AXIS_PERMUTATIONS: Callable[[], list[vec4]] = lambda: [
    vec4(),
    vec4(1.0),
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
