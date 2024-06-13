from src import *

""""""

import pytest

from src.math import get_line_to_line_transformation


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
        try:
            T = get_line_to_line_transformation(p1, p2, q1, q2)
            assert glm.distance(T @ p1, q1) < EPS
            assert glm.distance(T @ p2, q2) < EPS
        except:
            print(p1, p2, q1, q2, expect_error)
            assert False
# fmt: on
