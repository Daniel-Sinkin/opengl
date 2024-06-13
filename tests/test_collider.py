from src import *

""""""

import pytest

from src.collider import Ray, SphereCollider


def test_ray_initialization():
    origin = vec3(1)
    direction = vec3_x()
    length = 10
    ray = Ray(origin, direction, length)

    assert ray.origin == origin
    assert ray.direction == glm.normalize(direction)
    assert ray.length == length


def test_sphere_collider_initialization():
    center = vec3()
    radius = 5
    sphere = SphereCollider(center, radius)

    assert sphere.center == center
    assert sphere.radius == radius

    with pytest.raises(ValueError):
        SphereCollider(center, -1)


def test_distance_to_point_minimizer():
    origin = vec3()
    direction = vec3_x()
    ray = Ray(origin, direction)

    p = vec3(3, 4, 0)
    dist, t = ray.distance_to_point_minimizer(p)

    assert t == 3
    assert pytest.approx(dist, 0.001) == 4


def test_distance_to_point():
    origin = vec3()
    direction = vec3_x()
    ray = Ray(origin, direction)

    p = vec3(3.0, 4.0, 0)
    dist = ray.distance_to_point(p)

    assert pytest.approx(dist, 0.001) == 4


def test_check_for_collision_sphere():
    origin = vec3()
    direction = vec3_x()
    ray = Ray(origin, direction)

    center = vec3_x(5.0)
    radius = 1
    sphere = SphereCollider(center, radius)

    collision_point = ray.check_for_collision_sphere(sphere)

    assert collision_point is not None
    assert collision_point == vec3_x(5.0)


def test_check_for_collision_sphere_miss():
    origin = vec3()
    direction = vec3_x(1.0)
    ray = Ray(origin, direction)

    center = vec3_xy(5.0)
    radius = 1
    sphere = SphereCollider(center, radius)

    collision_point = ray.check_for_collision_sphere(sphere)

    assert collision_point is None


def test_sphere_collider_check_for_collision():
    origin = vec3()
    direction: vec3 = vec3_x()
    ray = Ray(origin, direction)

    center = vec3_x(5.0)
    radius = 1
    sphere = SphereCollider(center, radius)

    collision_point = sphere.check_for_collision(ray)

    assert collision_point is not None
    assert collision_point == (glm.distance(center - origin, ray.direction) <= radius)
