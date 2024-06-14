from . import *

""""""


class Ray:
    """
    Parametrized by the curve
    ```latex
    f(t) = o + t * v, 0 \leq t \leq \operatorname{length}
    ```
    or t is unbounded if length is None.
    """

    def __init__(self, origin: vec3, direction: vec3, length: Optional[float] = None):
        self.origin: vec3 = origin
        self.direction: vec3 = glm.normalize(direction)
        self.length: Optional[float] = length

    def __repr__(self):
        if self.length is None:
            return f"Ray(origin={self.origin},direction={self.direction})"
        else:
            return f"Ray(origin={self.origin},direction={self.direction},{self.length})"

    def __str__(self):
        return self.__repr__()

    def distance_to_point_minimizer(self, p: vec3) -> tuple[float, float]:
        t: float = glm.dot(p - self.origin, self.direction)
        # Only positive ray val is allowed
        t_: float = max(t, 0.0)
        return glm.distance(self.origin + t_ * self.direction, p), t_

    def distance_to_point(self, p: vec3) -> float:
        dist, _ = self.distance_to_point_minimizer(p)
        return dist

    def check_for_collision_sphere(self, obj: "SphereCollider") -> Optional[vec3]:
        # We're inside of the ball!
        if glm.distance(self.origin, obj.center) <= obj.radius:
            return self.origin
        dist, t = self.distance_to_point_minimizer(obj.center)
        if dist <= obj.radius:
            return self.origin + (t - obj.radius) * self.direction
        else:
            return None

    def check_for_collision(self, obj: "Collider") -> Optional[vec3]:
        if not isinstance(self, "Collider"):
            raise TypeError(f"Can't compute collision with {type(obj)}.")
        if not isinstance(obj, SphereCollider):
            raise NotImplementedError

        if isinstance(obj, SphereCollider):
            return self.check_for_collision_sphere(obj)


class Collider:
    @abstractmethod
    def check_for_collision(obj: "Collider | Ray") -> Optional[vec3]: ...


class SphereCollider(Collider):
    def __init__(self, center: vec3, radius: float):
        if radius <= 0:
            raise ValueError("SphereCollider must have positive radius.")
        self.radius = float(radius)

        self.center: vec3 = center

    def __repr__(self):
        return f"SphereCollider({self.center},{self.radius})"

    def __str__(self):
        return self.__repr__()

    def check_for_collision(self, obj: "Collider | Ray") -> Optional[vec3]:
        """If there is a collision then return collision point, otherwise return None."""
        if not isinstance(obj, Ray):
            raise NotImplementedError("Non-ray sphere collision is not supported yet.")

        return obj.check_for_collision_sphere(self)
