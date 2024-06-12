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
    """
    If we invoke glm.normalize on a zero vector then OpenGL itself crashes, so should always use this function.
    """
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


def clamp_vector_above(v: vec3, upper_bound: float, lower_bound: float = EPS) -> vec3:
    assert lower_bound < upper_bound

    normalized: vec3 = normalize_or_zero(v)
    if normalized == vec3():
        return normalized

    if glm.length(v) < lower_bound:
        return lower_bound * normalized

    if glm.length(v) > upper_bound:
        return upper_bound * normalized

    return v
