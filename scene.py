import typing

# TODO: Remove this wildcard import
from model import *
from src.constants import *

if typing.TYPE_CHECKING:
    from main import GraphicsEngine


class Scene:
    def __init__(self, app: "GraphicsEngine"):
        self.app: "GraphicsEngine" = app
        self.objects = []
        self.load_cat_circle()
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj) -> None:
        self.objects.append(obj)

    # TODO: Add serializing and deserializing to scenes
    #       Idea I had was to use the fact that we have 3 floats for each
    #       postion, rotation and scale, if we have n objects then we just have
    #       3 arrays of shape (n, 3) so we could just store them as a single (n, 3, 3)
    #       array by just stacking them, that would have the advantage that we
    #       can immediately read of the number of objects from the header.
    def load(self) -> None:
        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=vec3(x, -s, z)))
        self.add_object(Cat(self.app, pos=vec3(0, -1, -15)))

        self.add_object(MovingCube(self.app, pos=vec3(5, 5, 5), rot=0.002 * vec3_xy))

    def load_basic(self) -> None:
        n, s = 30, 3
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=vec3(x, -s, z)))
        self.add_object(Cat(self.app, pos=vec3(0, -2, -15)))

    def load_cat_circle(self) -> None:
        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=glm.vec3(x, -s, z)))

        for alpha in np.linspace(0, 2 * np.pi, 8):
            pos = glm.rotate((15.0, 0), alpha)
            self.add_object(
                Cat(
                    self.app,
                    pos=(pos.x, -1, pos.y),
                    rot=-float(alpha + np.pi / 2) * vec3_z,
                )
            )
            self.add_object(
                MovingCube(self.app, pos=vec3(pos.x, 12, pos.y), rot=0.002 * vec3_xy)
            )

    def load_basic_example(self) -> None:
        tex_ids: list[int] = [0, 1, 2, 0, 1, 2, 0]
        poss: list[vec3] = [
            vec3_0,
            -2.5 * vec3_x,
            2.5 * vec3_x,
            -5.0 * vec3_x,
            5.0 * vec3_x,
            -7.5 * vec3_x,
            7.5 * vec3_x,
        ]
        rots: list[vec3] = [
            vec3_0,
            45 * vec3_x,
            -45 * vec3_x,
            90 * vec3_x,
            -90 * vec3_x,
            135 * vec3_x,
            -135 * vec3_x,
        ]
        scales: list[vec3] = [
            vec3_1,
            0.75 * vec3_1,
            0.6 * vec3_1,
            0.5 * vec3_1,
            0.4 * vec3_1,
            0.3 * vec3_1,
            0.2 * vec3_1,
        ]

        for tex_id, pos, rot, scale in zip(tex_ids, poss, rots, scales):
            self.add_object(
                Cube(self.app, texture_id=tex_id, pos=pos, rot=rot, scale=scale)
            )

    def render(self) -> None:
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self) -> None: ...
