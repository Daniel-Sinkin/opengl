from src import *

""""""

import pytest

import src.math
from src.math import get_line_to_line_transformation, rel_to_abs_screenspace_coords


# fmt: off
@pytest.mark.parametrize(
    "p1, p2, q1, q2, expect_error", 
[
    (glm.vec3(0, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0), False),
    (glm.vec3(0, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0, 0), glm.vec3(2, 0, 0), False),
    (glm.vec3(0, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0), False),
    (glm.vec3(1, 1, 1), glm.vec3(2, 1, 1), glm.vec3(3, 3, 3), glm.vec3(4, 3, 3), False),
    (glm.vec3(1, 0, 0), glm.vec3(2, 0, 0), glm.vec3(0, 0, 1), glm.vec3(0, 0, 3), False),
    (glm.vec3(0, 0, 0), glm.vec3(0, 0, 0), glm.vec3(1, 1, 1), glm.vec3(1, 1, 1), True)
])
def test_get_line_to_line_transformation(p1, p2, q1, q2, expect_error) -> None:
    if expect_error:
        with pytest.raises(AssertionError):
            get_line_to_line_transformation(p1, p2, q1, q2)
    else:
        T = get_line_to_line_transformation(p1, p2, q1, q2)
        assert isinstance(T, mat4)
        assert glm.distance(T @ p1, q1) < EPS
        assert glm.distance(T @ p2, q2) < EPS

width = 1600
height = 900


@pytest.mark.parametrize(
    "width, height, rel_x, rel_y, expected", [
        (width, height, -1, -1, (0.0, height)),
        (width, height, -1, -1, (0.0, 0.0)),
        (width, height, -1, -1, (width, height)),
        (width, height, -1, -1, (width, 0.0)),
        (width, height, 0, 0, (800, 450)),
    ],
)
def test_rel_to_abs_screenspace_coords(width, height, rel_x, rel_y, expected) -> None:
    assert rel_to_abs_screenspace_coords(width, height, rel_x, rel_y) == expected
# fmt: on


def test_glm_reimplementation() -> None:
    # TODO: Implement the corresponding function and then remove the early return
    return
    _rng = np.random.default_rng(0x2024_06_14)

    vecs_array: np.ndarray = _rng.uniform(-1000.0, 1000.0, size=(1000, 3, 3))
    floats_array: np.ndarray = _rng.uniform(-1000.0, 1000.0, size=(1000, 4))

    func_tuple: list[tuple[Callable, Callable]] = [
        (glm.cross, src.math.cross),
        (glm.lookAt, src.math.lookAt),
        (glm.translate, src.math.translate),
        (glm.scale, src.math.scale),
    ]
    for vecs, floats in zip(vecs_array, floats_array):
        for glm_func, my_func in func_tuple:
            assert np.allclose(
                glm.cross(vecs[0], vecs[1]), src.math.cross(vecs[0], vecs[1])
            )
            assert np.allclose(glm.lookAt(*vecs), src.math.lookAt(*vecs))
            assert np.allclose(glm.perspective(*floats), src.math.perspective(*floats))
            assert np.allclose(glm.translate(vecs[0]), src.math.translate(vecs[0]))
            assert np.allclose(glm.scale(vecs[0]), src.math.scale(vecs[0]))
