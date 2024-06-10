import glm
from glm import mat4, vec3

from src.constants import *


class Light:
    def __init__(self, position=(50, 50, -10), color=(1, 1, 1)):
        self.position = vec3(position)
        self.color = vec3(color)
        self.direction = vec3_0
        # Ambient
        self.Ia = 0.06 * self.color
        # Diffuse
        self.Id = 0.8 * self.color
        # Specular
        self.Is = 1.0 * self.color

        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, vec3_y)
