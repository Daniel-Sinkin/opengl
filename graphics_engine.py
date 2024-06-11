import os
import sys
import typing
from logging import Logger
from typing import Optional

import moderngl as mgl
import ujson as json
from glm import vec3

# Suppresses welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

from src import my_logger
from src.camera import Camera
from src.constants import *
from src.light import Light
from src.mesh import Mesh
from src.model import Cube
from src.my_logger import setup
from src.opengl import setup_opengl
from src.player_controller import PlayerController
from src.scene import Scene
from src.scene_renderer import SceneRenderer
from src.settings import Colors, Settings_OpenGL


# TODO: Make GraphicsEngine a part of a larger application instead of being the first class object.
class GraphicsEngine:
    def __init__(self, win_size: Optional[tuple[int, int]] = None):
        self.logger: Logger = my_logger.setup("GraphicsEngine")

        self.window_size: tuple[int, int] = Settings_OpenGL.WINDOW_SIZE
        setup_opengl(window_size=self.window_size)

        self.ctx: mgl.Context = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.light = Light()
        self.camera = Camera(
            self,
        )
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

        self.is_running = True
        self.frame_counter = 0

        # TODO: Think about moving this to the camera
        self.camera_projection_has_changed = False
        self.mouse_position_on_freelook_enter = None

        self.player_controller_mode = PLAYER_CONTROLLER_MODE.FPS
        self.player_controller = PlayerController(self)

    def check_events(self) -> None:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.is_running = False
                case pg.MOUSEMOTION:
                    # Only move the camera if in FPS mode.
                    if self.player_controller_mode in (
                        PLAYER_CONTROLLER_MODE.FLOATING_CAMERA,
                        PLAYER_CONTROLLER_MODE.FPS,
                    ):
                        mouse_rel: tuple[int, int] = typing.cast(
                            tuple[int, int], event.rel
                        )
                        if mouse_rel != (0, 0):
                            self.camera.rotate(*mouse_rel)

                            pg.mouse.set_pos(
                                (self.window_size[0] // 2, self.window_size[1] // 2)
                            )
                            # Flushes the mouse position buffer
                            pg.mouse.get_rel()
                case pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.player_controller_mode = (
                            PLAYER_CONTROLLER_MODE.UNLOCKED_MOUSE
                        )
                        if self.mouse_position_on_freelook_enter is not None:
                            pg.mouse.set_pos(self.mouse_position_on_freelook_enter)
                            self.mouse_position_on_freelook_enter = None

                        pg.event.set_grab(False)
                        pg.mouse.set_visible(True)
                    if event.key == pg.K_SPACE:
                        self.camera.reset_to_inital_state()
                case pg.MOUSEBUTTONDOWN:
                    if (
                        self.player_controller_mode
                        == PLAYER_CONTROLLER_MODE.UNLOCKED_MOUSE
                        and event.button
                        in (
                            pg.BUTTON_LEFT,
                            pg.BUTTON_RIGHT,
                            pg.BUTTON_MIDDLE,
                        )
                    ):
                        # Avoids sudden jumps when re-entering FPS mode
                        _ = pg.mouse.get_rel()

                        self.mouse_position_on_freelook_enter: tuple[int, int] = (
                            pg.mouse.get_pos()
                        )

                        self.player_controller_mode = (
                            PLAYER_CONTROLLER_MODE.FLOATING_CAMERA
                        )
                        pg.event.set_grab(True)
                        pg.mouse.set_visible(False)
                    if event.button == pg.BUTTON_WHEELDOWN:
                        self.camera.adjust_fov(5)
                    if event.button == pg.BUTTON_WHEELUP:
                        self.camera.adjust_fov(-5)

    def render(self) -> None:
        # This should always be covered
        self.ctx.clear(color=Colors.MISSING_TEXTURE)

        self.scene_renderer.render()

        pg.display.flip()

    def get_time(self) -> None:
        self.time = pg.time.get_ticks() * MS_TO_SECOND

    def pre_run(self) -> None:
        self.camera.activate_recording(5 * SECOND_TO_MS)

    def run(self) -> None:
        while self.is_running:
            self.get_time()
            self.check_events()

            if self.player_controller_mode == PLAYER_CONTROLLER_MODE.FLOATING_CAMERA:
                self.camera.move()
            elif self.player_controller_mode == PLAYER_CONTROLLER_MODE.FPS:
                self.player_controller.move()

            self.camera.update()
            self.player_controller.update()
            self.render()
            self.delta_time: int = self.clock.tick(60.0)

            self.frame_counter += 1

            self.camera_projection_has_changed = False

    def __del__(self) -> None:
        self.logger.info("Cleaning up Graphics Enging.")
        try:
            self.mesh.destroy()
        except AttributeError:
            self.logger.warn("Didn't have a mesh when getting destroyed.")
        pg.quit()

        self.logger.info("Cleanup is done, deleting logger now.")
        my_logger.cleanup(self.logger)


def main() -> None:
    graphics_engine = GraphicsEngine()
    graphics_engine.run()


if __name__ == "__main__":
    main()
