from . import *

"""
This serves both as a utility class and as me implementing the blackbox functions that I use from
glm like how the translation, scaling and rotation matrices are constructed, how view projection,
model projections and so on are done under the hood.

Maybe I'll split up the utility functionality and the "re-implementation" into seperate files as 
my reimplementation will be quite a bit slower than the native glm operations.
"""

###
# Math Utilities
###


def get_line_to_line_transformation(p1: vec3, p2: vec3, q1: vec3, q2: vec3) -> mat4:
    """
    Returns the matrix T such that T @ p1 = q1, T @ p2 = q2
    """
    dist_q: float = glm.distance(q1, q2)
    dist_p: float = glm.distance(p1, p2)
    assert dist_p > EPS, "The points have to be different"
    assert dist_q > EPS, "The points have to be different"

    direction_p: vec3 = glm.normalize(p2 - p1)
    direction_q: vec3 = glm.normalize(q2 - q1)

    # How much will we need to stretch the line
    scaling_factor: float = dist_q / dist_p

    scaling_matrix: mat4 = glm.scale(vec3(scaling_factor))

    rotation_axis: vec3 = glm.cross(direction_p, direction_q)
    if glm.distance(rotation_axis, vec3()) < EPS:
        rotation_matrix = mat4()
    else:
        rotation_angle: float = glm.acos(glm.dot(direction_p, direction_q))
        rotation_matrix: mat4 = glm.rotate(rotation_angle, rotation_axis)

    return glm.translate(q1) @ rotation_matrix @ scaling_matrix @ glm.translate(-p1)


def distance_line_to_point(p1: vec3, p2: vec3, q: vec3) -> float:
    """Unbounded Line to point distance, computed by projecting v onto p - ray_0."""
    q_offset: vec3 = q - p1
    ray_dir_n: vec3 = glm.normalize(p2 - p1)
    return glm.distance(glm.dot(ray_dir_n, q_offset) * ray_dir_n, q_offset)


def ndc_to_screenspace(x, y, width, height) -> tuple[int, int]:
    return int((x + 1.0) / 2.0 * width), int((-y + 1.0) / 2.0 * height)


def screenspace_to_ndc(x, y, width, height) -> tuple[float, float]:
    return 2.0 * x / width - 1.0, 1.0 - 2.0 * y / height


###
# Reimplementations
###


def cross(p: vec3, q: vec3) -> vec3:
    s1: float = p.y * q.z - p.z * q.y
    s2: float = p.z * q.x - p.x * q.z
    s3: float = p.x * q.y - p.y * q.x
    return vec3(s1, s2, s3)


def lookAt(self, eye: vec3, center: vec3, up: vec3) -> mat4: ...


def perspective(self, fovy: float, aspect: float, near: float, far: float) -> mat4: ...


# fmt: off
def translate(v: vec3) -> mat4:
    """Returns a matrix T such that vec3(T @ p) = (p.x + v.x, p.y + v.y, p.z + v.z)."""
    return mat4(
        1.0, 0.0, 0.0, v.x,
        0.0, 1.0, 0.0, v.y,
        0.0, 0.0, 1.0, v.z,
        0.0, 0.0, 0.0, 1.0
    )

def scale(v: vec3) -> mat4:
    """Returns a matrix T such that vec3(T @ p) = (v.x * p.x, v.y * p.y, v.z * p.z)."""
    return mat4(
        v.x, 0.0, 0.0, 0.0,
        0.0, v.y, 0.0, 0.0,
        0.0, 0.0, v.z, 0.0,
        0.0, 0.0, 0.0, 1.0
    )

# TODO: Implement the case where we have rotation axis and angle given.
def get_axis_rotation_matrix(angles: vec3) -> mat4:
    """Returns a rotation matrix for rotating around the corresponding angles around each axis."""
    c_x, s_x = glm.cos(angles.x), glm.sin(angles.x)
    c_y, s_y = glm.cos(angles.y), glm.sin(angles.y)
    c_z, s_z = glm.cos(angles.z), glm.sin(angles.z)
    rot_x = mat4(
         1.0,  0.0,  0.0,  0.0,
         0.0,  c_x,  s_x,  0.0,
         0.0, -s_x,  c_x,  0.0,
         0.0,  0.0,  0.0,  1.0,
    )
    rot_y = mat4(
         c_y,  0.0,  s_y,  0.0,
         0.0,  1.0,  0.0,  0.0,
        -s_y,  0.0,  c_y,  0.0,
         0.0,  0.0,  0.0,  1.0,
    )
    rot_z = mat4(
         c_z,  s_z,  0.0,  0.0,
        -s_z,  c_z,  0.0,  0.0,
         0.0,  0.0,  1.0,  0.0,
         0.0,  0.0,  0.0,  1.0,
    )
    return rot_z @ rot_y @ rot_x
# fmt: on


def mat4_x_vec3_to_vec3(M: mat4, v: vec3) -> vec3:
    """
    This is what gets executed when you call M @ v.
    """
    v_extended = vec4(*v, 1)
    product: vec4 = M @ v_extended
    product_restricted = vec3(product)
    return product
