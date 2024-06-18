from src import *

""""""

import pytest

import src.math
from src.math import (
    get_line_to_line_transformation,
    ndc_to_screenspace,
    screenspace_to_ndc,
)

WIDTH = 1367
HEIGHT = 821

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

@pytest.mark.parametrize(
    "x, y, width, height, expected", [
        (0, 0, WIDTH, HEIGHT, (-1.0, 1.0)),              # Top-left corner
        (WIDTH, 0, WIDTH, HEIGHT, (1.0, 1.0)),           # Top-right corner
        (0, HEIGHT, WIDTH, HEIGHT, (-1.0, -1.0)),        # Bottom-left corner
        (WIDTH, HEIGHT, WIDTH, HEIGHT, (1.0, -1.0)),     # Bottom-right corner
        (WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT, (0.0, 0.0)), # Center
    ],
)
def test_screenspace_to_ndc(x, y, width, height, expected) -> None:
    assert screenspace_to_ndc(x, y, width, height) == expected

@pytest.mark.parametrize(
    "ndc_x, ndc_y, width, height, expected", [
        (-1.0, 1.0, WIDTH, HEIGHT, (0, 0)),              # Top-left corner
        (1.0, 1.0, WIDTH, HEIGHT, (WIDTH, 0)),           # Top-right corner
        (-1.0, -1.0, WIDTH, HEIGHT, (0, HEIGHT)),        # Bottom-left corner
        (1.0, -1.0, WIDTH, HEIGHT, (WIDTH, HEIGHT)),     # Bottom-right corner
        (0.0, 0.0, WIDTH, HEIGHT, (WIDTH // 2, HEIGHT // 2)), # Center
    ],
)
def test_ndc_to_screenspace(ndc_x, ndc_y, width, height, expected) -> None:
    assert ndc_to_screenspace(ndc_x, ndc_y, width, height) == expected
# fmt: on


def test_ndc_screenspace_inverse_invariance():
    """Test that the functions are inverses of each other."""
    n_samples = 1_000
    _rng = np.random.default_rng(0x2024_06_19)
    ints = _rng.integers((0, 0), (WIDTH + 1, HEIGHT + 1), size=(1000, 2))
    for x, y in ints:
        screen_x, screen_y = ndc_to_screenspace(
            *screenspace_to_ndc(x, y, WIDTH, HEIGHT), WIDTH, HEIGHT
        )

        # Allow 1 pixel offset due to rounding errors
        assert abs(screen_x - x) <= 1
        assert abs(screen_y - y) <= 1


@pytest.mark.slow
def test_ndc_screenspace_inverse_invariance_slow():
    """Test that the functions are inverses of each other for all possible screen coordinates."""
    for x in range(WIDTH + 1):
        for y in range(HEIGHT + 1):
            x_, y_ = ndc_to_screenspace(
                *screenspace_to_ndc(x, y, WIDTH, HEIGHT), WIDTH, HEIGHT
            )

            # Allow 1 pixel offset due to rounding errors
            assert abs(x_ - x) <= 1, f"computed x: {x_}, actual x: {x}"
            assert abs(y_ - y) <= 1, f"computed y: {y_}, actual y: {y}"


def test_glm_reimplementation() -> None:
    # TODO: Implement the corresponding function and then remove the early return
    return
    _rng = np.random.default_rng(0x2024_06_14)

    combined_array = _rng.uniform(-1000.0, 1000.0, size=(1000, 3, 3 + 4))

    vecs_array = combined_array[:, :, :3]
    floats_array = combined_array[:, :, 3:].reshape(1000, 4)

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
