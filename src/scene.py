import random
import typing

from .constants import *
from .model import *

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine


class Scene:
    def __init__(self, app: "GraphicsEngine"):
        self.app: GraphicsEngine = app
        # Tracks a unique index for every object
        self.object_idx = 0
        self.objects: list[Model] = []

        self.load_cat_circle_animated_scale()
        self.skybox = SkyBox(app)

    def serialize(
        self, serialize_type="json", filepath=None
    ) -> dict[int, BASEMODEL_SERIALIZE]:
        if serialize_type != "json":
            raise NotImplementedError(
                DevStringsLambda.UNSUPPORTED_OBJECT_SERIALIZATION_TYPE(serialize_type)
            )
        dict_: dict[int, BASEMODEL_SERIALIZE] = {
            obj.scene_idx: obj.serialize(
                serialize_type, filepath=None, include_scene_idx=False
            )
            for obj in self.objects
        }

    def add_object(self, obj: Model, log=False) -> None:
        log = True
        self.objects.append(obj)
        obj.scene_idx = self.object_idx
        if log:
            self.app.logger.debug("Registered object: %s", obj)

        self.object_idx += 1

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
                self.add_object(
                    Cube(
                        self.app,
                        tex_id=(x + z) % 3,
                        pos=vec3(x, -s, z),
                    )
                )
        self.add_object(Cat(self.app, pos=vec3(0, -1, -15)))

        self.add_object(Cube(self.app, pos=vec3(5, 5, 5), rot_update=0.002 * vec3_xy()))

    def load_basic(self) -> None:
        n, s = 30, 3
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=vec3(x, -s, z)))
        self.add_object(Cat(self.app, pos=vec3(0, -2, -15)))

    def load_cat_circle_animated_scale(self) -> None:
        n, s = 80, 2
        for i, x in enumerate(range(-n, n + 1, s)):
            for j, z in enumerate(range(-n, n + 1, s)):
                self.add_object(
                    Cube(
                        self.app,
                        tex_id=(i + j) % 3,
                        pos=glm.vec3(
                            x,
                            -2 + 4 * max(0, max(abs(x), abs(z)) - (n - 30)),
                            z,
                        ),
                        rot_update=2.5 * random.choice(VEC3_AXIS_PERMUTATIONS()),
                    )
                )

        def cat_scale_func(sigma):
            return 0.5 * (1 + glm.cos(2 * sigma)) * (vec3_1()) + 0.5 * (
                1 - glm.cos(2 * sigma)
            ) * (vec3_xy() + 0.3 * vec3_z())

        for alpha in np.linspace(0, 2 * np.pi, 15 + 1)[:-1]:
            alpha_normalized = alpha / (2 * np.pi)
            pos = glm.rotate((15.0, 0), alpha)
            cat = Cat(
                self.app,
                pos=(pos.x, -1, pos.y),
                rot=-float(alpha + np.pi / 2) * vec3_z(),
            )
            cat.alpha = alpha
            cat.scale_animation_function = lambda x: cat_scale_func(x)
            self.add_object(cat)
            self.add_object(
                Cube(self.app, pos=vec3(pos.x, 12, pos.y), rot_update=2.5 * vec3_xy())
            )

    def load_cat_circle(self) -> None:
        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=glm.vec3(x, -s, z)))

        for alpha in np.linspace(0, 2 * np.pi, 15 + 1)[:-1]:
            alpha_normalized = alpha / (2 * np.pi)
            pos = glm.rotate((15.0, 0), alpha)
            self.add_object(
                Cat(
                    self.app,
                    pos=(pos.x, -1, pos.y),
                    rot=-float(alpha + np.pi / 2) * vec3_z(),
                )
            )
            self.add_object(
                Cube(self.app, pos=vec3(pos.x, 12, pos.y), rot_update=2.5 * vec3_xy())
            )

    def load_basic_example(self) -> None:
        tex_ids: list[int] = [0, 1, 2, 0, 1, 2, 0]
        poss: list[vec3] = [
            vec3_0(),
            -2.5 * vec3_x(),
            2.5 * vec3_x(),
            -5.0 * vec3_x(),
            5.0 * vec3_x(),
            -7.5 * vec3_x(),
            7.5 * vec3_x(),
        ]
        rots: list[vec3] = [
            vec3_0(),
            45 * vec3_x(),
            -45 * vec3_x(),
            90 * vec3_x(),
            -90 * vec3_x(),
            135 * vec3_x(),
            -135 * vec3_x(),
        ]
        scales: list[vec3] = [
            vec3_1(),
            0.75 * vec3_1(),
            0.6 * vec3_1(),
            0.5 * vec3_1(),
            0.4 * vec3_1(),
            0.3 * vec3_1(),
            0.2 * vec3_1(),
        ]

        for tex_id, pos, rot, scale in zip(tex_ids, poss, rots, scales):
            self.add_object(
                Cube(self.app, texture_id=tex_id, pos=pos, rot=rot, scale=scale)
            )

    def render(self) -> None:
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self) -> None:
        for obj in self.objects:
            obj.update()
