from . import *

"""
This holds specific constants for different parts of the code in a centralized way, should not be
wildcard imported, unlike the `globals.py` file.
"""


###
# Strings
###
@dataclass
class VBO:
    IN_TEXCOORD_N: Callable[[int], str] = lambda n: f"in_texcoord_{n}"
    IN_TEXCOORD_0: str = IN_TEXCOORD_N(0)
    IN_TEXCOORD_1: str = IN_TEXCOORD_N(1)
    IN_TEXCOORD_2: str = IN_TEXCOORD_N(2)
    IN_NORMAL = "in_normal"
    IN_POSITION = "in_position"
    IN_COLOR = "in_color"

    FILE_CUBE = "CubeVBO.npy"
    FILE_CYLINDER = "CylinderVBO.npy"
    FILE_SPHERE = "SphereVBO.npy"


###
# Enums
###
class PLAYER_CONTROLLER_MODE(IntEnum):
    FLOATING_CAMERA = auto()
    MENU = auto()
    FPS = auto()


###
# Dicts
###
class CameraSerializeBase(TypedDict):
    position: POSITION3D
    pitch: float
    yaw: float


class CameraSerialize(CameraSerializeBase):
    near_plane: float
    far_plane: float
    speed: float
    sensitivity: float


class BasemodelSerialize(TypedDict):
    vao_name: str
    texture_id: int
    pos: POSITION3D
    rot: POSITION3D
    scale: POSITION3D


class ModelSerialize(BasemodelSerialize):
    rot_update: POSITION3D


SCENE_SERIALIZE_DICT: TypeAlias = dict[int, BasemodelSerialize]
