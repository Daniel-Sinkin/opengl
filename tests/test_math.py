from src import *

""""""

import pytest

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
def test_get_line_to_line_transformation(p1, p2, q1, q2, expect_error):
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
def test_rel_to_abs_screenspace_coords(width, height, rel_x, rel_y, expected):
    assert rel_to_abs_screenspace_coords(width, height, rel_x, rel_y) == expected
# fmt: on
