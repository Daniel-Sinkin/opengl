from . import *

"""
My utility math library, I might rewrite all the black box glm operations I'm using (like
the projection, look_at, translation, scaling, rotation and so on) in here, but I prolly should
stick to the std implementation regardless for performance reasons.
"""


def dot(p: vec3, q: vec3) -> vec3:
    return sum(p * q)


def length(p: vec3) -> float:
    return glm.sqrt(dot(p, p))


def length2(p: vec3) -> float:
    return dot(p, p)


def norm1(p: vec3) -> float:
    return abs(p.x) + abs(p.y) + abs(p.z)


def norm_inf(p: vec3) -> float:
    return max(abs(p.x), abs(p.y), abs(p.z))


def normalize(p: vec3) -> vec3:
    return p / length(p)


def cross(p: vec3, q: vec3) -> vec3:
    s1: float = p.y * q.z - p.z * q.y
    s2: float = p.z * q.x - p.x * q.z
    s3: float = p.x * q.y - p.y * q.x
    return vec3(s1, s2, s3)


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

def rot_angle_vector(angles: vec3) -> mat4:
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


def get_line_transform_from_endpoints(p: vec3, q: vec3) -> mat4:
    """
    Computes T such that T @ (0, 0, 0) = p, T @ (1, 0, 0) = q.
    """

    # It's not faster to compute distance and divide it rather than normalizing via that function.
    distance = glm.distance(p, q)
    if distance < EPS:
        raise ValueError("Can't put a line between a point and itself!")

    direction = glm.normalize(q - p)

    translation_matric: mat4 = glm.translate(glm.mat4(), p)

    scaling_matrix: mat4 = glm.scale(glm.mat4(), glm.vec3(distance, 1.0, 1.0))

    angle: float = glm.acos(direction.x)
    rotation_axis: vec3 = glm.cross(vec3_x(), direction)

    if glm.length(rotation_axis) > EPS:
        rotation_axis = glm.normalize(rotation_axis)
        rotation_matrix = glm.rotate(glm.mat4(1.0), angle, rotation_axis)
    else:
        rotation_matrix = glm.mat4(1.0)

    transformation_matrix = translation_matric * rotation_axis * scaling_matrix

    start_point = vec4_w()
    end_point = vec4_xw()

    transformed_start_point = transformation_matrix * start_point
    transformed_end_point = transformation_matrix * end_point

    print(transformed_start_point, transformed_end_point)


# TODO: Think of a better name this is horrible
def mat4_x_vec3_to_vec3(M: mat4, v: vec3) -> vec3:
    v_extended = vec4(*v, 1)
    product: vec4 = M @ v_extended
    product_restricted = vec3(product)
    return product
