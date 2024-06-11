import glm
from glm import mat4, vec3

from .constants import *


# https://learnopengl.com/Advanced-Lighting/Advanced-Lighting
class Light:
    def __init__(self, position=(50, 50, -10), color=(1, 1, 1)):
        self.position = vec3(position)
        self.color = vec3(color)
        self.direction: vec3 = vec3_0

        self.intensity_ambient: vec3 = 0.06 * self.color
        self.intensity_diffuse: vec3 = 0.8 * self.color
        self.intensity_specular: vec3 = 1.0 * self.color

        self.m_view_light: mat4 = self.get_view_matrix()

    def get_view_matrix(self) -> mat4:
        return glm.lookAt(self.position, self.direction, vec3_y)
