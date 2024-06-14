from src import *

""""""

import pytest

from src.collider import Ray, SphereCollider


def test_sphere_collider_initialization():
    with pytest.raises(ValueError):
        SphereCollider(vec3(), -1.0)


def test_distance_to_point_minimizer_local_minimum() -> None:
    """
    Tests the projection invariant that any offset from the projection increases the distance,
    i.e. the parametrized distance function has a local minimum.
    """
    ray = Ray(vec3(), vec3_x())
    p_0 = vec3(3.0, 4.0, 0.0)

    dist_0, t = ray.distance_to_point_minimizer(p_0)

    assert np.isclose(t, 3.0)
    assert np.isclose(dist_0, 4.0)

    _rng = np.random.default_rng(0x2024_06_14)
    random_floats = _rng.uniform(-1000.0, 1000.0, (1000, 3, 3))
    for rands in random_floats:
        origin = vec3(rands[0])
        direction = vec3(rands[1])
        ray = Ray(origin, direction)

        p = vec3(rands[2])
        dist, t = ray.distance_to_point_minimizer(p)

        if t >= 0.01:
            t_minus = t - 0.01
            dist_minus = glm.distance(origin + t_minus * direction, p)
            assert dist_minus > dist

        t_plus = t + 0.01
        dist_plus = glm.distance(origin + t_plus * direction, p)

        assert dist_plus > dist


def test_check_for_collision_sphere():
    origin = vec3()
    direction = vec3_x()
    ray = Ray(origin, direction)

    center = vec3_x(5.0)
    radius = 1.0
    sphere = SphereCollider(center, radius)

    collision_point = ray.check_for_collision_sphere(sphere)

    assert collision_point is not None
    assert np.isclose(glm.distance(collision_point, vec3_x(5.0)), radius)


def test_check_for_collision_sphere_miss():
    origin = vec3()
    direction = vec3_x(1.0)
    ray = Ray(origin, direction)

    center = vec3_xy(5.0)
    radius = 1.0
    sphere = SphereCollider(center, radius)

    collision_point = ray.check_for_collision_sphere(sphere)
    assert collision_point is None


def test_sphere_collider_check_for_collision():
    origin = vec3()
    direction: vec3 = vec3_x()
    ray = Ray(origin, direction)

    center = vec3_x(5.0)
    radius = 1.0
    sphere = SphereCollider(center, radius)

    collision_point = sphere.check_for_collision(ray)

    assert collision_point is not None
    assert glm.distance(vec3_x(4.0), collision_point) < EPS
