from typing import overload

import glm
from glm import vec1, vec2, vec3, vec4

from .constants import *


@overload
def normalize_or_zero(v: vec1, atol: float = 1e-4) -> vec1: ...
@overload
def normalize_or_zero(v: vec2, atol: float = 1e-4) -> vec2: ...
@overload
def normalize_or_zero(v: vec3, atol: float = 1e-4) -> vec3: ...
@overload
def normalize_or_zero(v: vec4, atol: float = 1e-4) -> vec4: ...


def normalize_or_zero(v: VEC_N, atol: float = EPS) -> VEC_N:
    if glm.length(v) < atol:
        if isinstance(v, vec1):
            return vec1(0)
        elif isinstance(v, vec2):
            return vec2(0, 0)
        elif isinstance(v, vec3):
            return vec3(0, 0, 0)
        elif isinstance(v, vec4):
            return vec4(0, 0, 0, 0)
    else:
        return glm.normalize(v)
