from . import *

""""""

from . import settings
from .constants import (
    PLAYER_CONTROLLER_MODE,
    CameraSerialize,
    CameraSerializeBase,
    DevStrings,
)

if TYPE_CHECKING:
    from .graphics_engine import GraphicsEngine


class Camera:
    def __init__(
        self,
        app: "GraphicsEngine",
        position: POSITION3D = None,
        yaw=settings.Camera.INITIAL_YAW,
        pitch=settings.Camera.INITAL_PITCH,
    ):
        self.app: GraphicsEngine = app
        self.aspect_ratio: float = app.window_size[0] / app.window_size[1]

        if position is not None:
            self.initial_position: POSITION3D = position
        else:
            self.initial_position: POSITION3D = settings.Camera.INITIAL_POSITION

        self.position = vec3(self.initial_position)

        # What we reset the fov to.
        self.original_fov = settings.Camera.FOV
        self.fov: float = self.original_fov

        self.near_plane: float = settings.Camera.NEAR
        self.far_plane: float = settings.Camera.FAR
        self.speed: float = settings.Camera.SPEED
        self.speed_turbo: float = settings.Camera.SPEED_TUROB
        self.sensitivity: float = settings.Camera.SENSITIVITY

        self.up: vec3 = vec3_y()
        self.right: vec3 = vec3_x()
        self.forward: vec3 = -vec3_z()

        self.initial_yaw, self.initial_pitch = yaw, pitch
        self.yaw, self.pitch = yaw, pitch

        self.m_view: mat4 = self.get_view_matrix()
        self.m_proj: mat4 = self.get_projection_matrix()

        self.recording_start = None
        self.is_recording = False

        self.recording_buffer: list[tuple[int, CameraSerializeBase]] = []
        self.recorded_camera_path_tracer = None

    def serialize(
        self,
        serialize_type="json",
        filepath: Optional[str] = None,
        include_base_settings=False,
    ) -> CameraSerializeBase:
        if serialize_type != "json":
            raise NotImplementedError(
                DevStrings.UNSUPPORTED_OBJECT_SERIALIZATION_TYPE(serialize_type)
            )

        dict_ = CameraSerializeBase(
            position=tuple(map(lambda x: round(x, 4), self.position)),
            pitch=round(self.pitch, 4),
            yaw=round(self.yaw, 4),
        )
        if include_base_settings:
            dict_["near_plane"] = round(self.near_plane, 4)
            dict_["far_plane"] = round(self.far_plane, 4)
            dict_["speed"] = round(self.speed, 4)
            dict_["sensitivity"] = round(self.sensitivity, 4)
            dict_ = cast(CameraSerialize, dict_)

        if filepath is not None:
            json.dump(dict_, filepath)

        return dict_

    def deserialize(self, serialized: CameraSerializeBase) -> None:
        self.position = vec3(serialized["position"])
        self.yaw = serialized["yaw"]
        self.pitch = serialized["pitch"]

    def append_current_to_path_trace(self) -> list[CameraSerializeBase]:
        self.path_trace[pg.time.get_ticks()] = self.serialize(
            serialize_type="json", filepath=None, include_base_settings=False
        )

    def rotate(self, rel_x, rel_y) -> None:
        self.yaw += rel_x * self.sensitivity
        self.pitch -= rel_y * self.sensitivity

        self.pitch = cast(float, glm.clamp(self.pitch, *settings.Camera.PITCH_BOUNDS))

    def update_camera_vectors(self) -> None:
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def _update_recoding(self) -> None:
        current_tick = pg.time.get_ticks()
        time_passed = current_tick - self.recording_start

        if time_passed < self.recording_duration_ms:
            self.recording_buffer.append(current_tick, self.serialize())
        else:
            dt_str = dt.datetime.now(tz=dt.timezone.utc).strftime(
                settings.Camera.RECORDING_TIME_FORMAT
            )
            with open(
                os.path.join(settings.Folders.RECORDINGS_CAMERA, dt_str), "w"
            ) as file:
                file.write(self.recording_buffer)

    def update(self) -> None:
        self.update_camera_vectors()
        if self.app.camera_projection_has_changed:
            self.m_proj: mat4 = self.get_projection_matrix()
        self.m_view: mat4 = self.get_view_matrix()

        if self.is_recording:
            self._update_recoding()

    def move(self) -> None:
        """
        When controlling a floating camera we can just pass through objects so we
        don't need any bound checks.
        """
        keys: pg.ScancodeWrapper = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.app.player_controller_mode = PLAYER_CONTROLLER_MODE.FPS
            return

        if keys[pg.K_LSHIFT]:
            velocity: float = self.speed_turbo * self.app.delta_time
        else:
            velocity: float = self.speed * self.app.delta_time

        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_UP]:
            self.position += self.up * velocity
        if keys[pg.K_DOWN]:
            self.position -= self.up * velocity

    def get_view_matrix(self) -> mat4:
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self) -> mat4:
        return glm.perspective(
            glm.radians(self.fov),
            self.aspect_ratio,
            self.near_plane,
            self.far_plane,
        )

    def reset_to_inital_state(self) -> None:
        """
        Moves and resets the camera to the state it had when initialized.
        """
        self.position = vec3(self.initial_position)
        self.yaw, self.pitch = (
            self.initial_yaw,
            self.initial_pitch,
        )
        self.fov = self.original_fov
        self.camera_projection_has_changed = True

    def adjust_fov(self, amount: float) -> None:
        """
        Increase or decrease the fov (within the bounds), usually called from
        the MOUSEWHEEL(UP/DOWN) event.
        """

        new_fov = cast(
            float,
            glm.clamp(self.fov + amount, *settings.Camera.FOV_BOUNDS),
        )
        if new_fov != self.fov:
            self.app.camera_projection_has_changed = True
            self.fov = new_fov

    def activate_recording(self, duration_ms: int) -> None:
        """
        Traces the camera transforms for a certain while, this functionality is pretty bare bones
        right now, ideal state would be that I can trace the camera with a frameskip and then
        interpolate later on, maybe making highly smooth playbacks or something like that.

        This is pretty closely related to what it would like to serialize the camera the entire
        time we are recording so maybe I could make some kind of short term serialization so we
        can add a playback, although that is something that comes much later, if at all.
        """

        self.recording_duration_ms: int = duration_ms
        self.recording_start: int = pg.time.get_ticks()
        self.is_recording = True
