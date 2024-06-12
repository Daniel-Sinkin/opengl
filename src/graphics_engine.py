import datetime as dt
import os
import sys
import typing
from logging import Logger
from typing import Optional

import moderngl as mgl
import numpy as np
import ujson as json
from freetype import Face
from glm import vec3
from PIL import Image

# Suppresses welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

from . import my_logger, settings
from .camera import Camera
from .constants import *
from .light import Light
from .mesh import Mesh
from .my_logger import setup
from .opengl import setup_opengl
from .player_controller import PlayerController
from .scene import Scene
from .scene_renderer import SceneRenderer


# TODO: Make GraphicsEngine a part of a larger application instead of being the first class object.
class GraphicsEngine:
    def __init__(self, win_size: Optional[tuple[int, int]] = None):
        self.logger: Logger = my_logger.setup("GraphicsEngine")

        self.window_size: tuple[int, int] = settings.OpenGL.WINDOW_SIZE
        self.pg_window = setup_opengl(window_size=self.window_size)

        # Locks mouse into window
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx: mgl.Context = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0.0
        self.delta_time = 0
        self.delta_time_s = 0

        # TODO: Set this in setting
        # TODO: Either include a free-license font or pull from internet, or make the
        #       font finder more os independent.
        self.font_face = Face(settings.UI.FONT_FILEPATH)
        self.font_face.set_char_size(settings.UI.FONT_CHARSIZE)

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

        self.take_screenshot_after_render = False

        # TODO: Add a dedicated State Management function instead of just swapping around
        self.player_controller_mode = PLAYER_CONTROLLER_MODE.FPS
        self.previous_player_controller_mode = PLAYER_CONTROLLER_MODE.FPS

        self.menu_open = self.player_controller_mode == PLAYER_CONTROLLER_MODE.MENU

        self.player_controller = PlayerController(self)

        # TODO: Once we have more sounds structure this better
        self.sound_state_transition = pygame.mixer.Sound(
            os.path.join(settings.Folders.DATA_SOUND, "state_transition.wav")
        )
        self.sound_screenshot = pygame.mixer.Sound(
            os.path.join(settings.Folders.DATA_SOUND, "screenshot.wav")
        )

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
                    if event.key in (pg.K_ESCAPE, pg.K_TAB):
                        if self.player_controller_mode != PLAYER_CONTROLLER_MODE.MENU:
                            self.sound_state_transition.play()
                            self.player_controller_mode = PLAYER_CONTROLLER_MODE.MENU
                            self.menu_open = True

                        if self.mouse_position_on_freelook_enter is not None:
                            pg.mouse.set_pos(self.mouse_position_on_freelook_enter)
                            self.mouse_position_on_freelook_enter = None

                        pg.event.set_grab(False)
                        pg.mouse.set_visible(True)
                    if event.key == pg.K_F1:
                        if (
                            self.player_controller_mode
                            != PLAYER_CONTROLLER_MODE.FLOATING_CAMERA
                        ):
                            self.sound_state_transition.play()
                            self.player_controller_mode = (
                                PLAYER_CONTROLLER_MODE.FLOATING_CAMERA
                            )
                case pg.KEYUP:
                    if event.key == pg.K_PRINTSCREEN:
                        self.take_screenshot_after_render = True
                case pg.MOUSEBUTTONDOWN:
                    if (
                        self.player_controller_mode == PLAYER_CONTROLLER_MODE.MENU
                        and event.button
                        in (
                            pg.BUTTON_LEFT,
                            pg.BUTTON_RIGHT,
                            pg.BUTTON_MIDDLE,
                        )
                    ):
                        self.sound_state_transition.play()
                        # Avoids sudden jumps when re-entering FPS mode
                        _ = pg.mouse.get_rel()

                        self.mouse_position_on_freelook_enter: tuple[int, int] = (
                            pg.mouse.get_pos()
                        )

                        self.player_controller_mode = (
                            self.previous_player_controller_mode
                        )
                        pg.event.set_grab(True)
                        pg.mouse.set_visible(False)
                        self.menu_open = False
                    if event.button == pg.BUTTON_WHEELDOWN:
                        self.camera.adjust_fov(5)
                    if event.button == pg.BUTTON_WHEELUP:
                        self.camera.adjust_fov(-5)

    # We should have game logic seperate from the rending logic, but everything
    # being synced with the rendering pipeline is okay for now.
    def render(self) -> None:
        # This should always be covered
        self.ctx.clear(color=settings.Colors.MISSING_TEXTURE)

        self.scene_renderer.render()

        if self.take_screenshot_after_render:
            self.take_screenshot_after_render = False
            self.take_screenshot()

        pg.display.flip()

    def get_time(self) -> None:
        self.time = pg.time.get_ticks() * MS_TO_SECOND

    def pre_run(self) -> None:
        self.camera.activate_recording(5 * SECOND_TO_MS)

    def run(self) -> None:
        while self.is_running:
            self.get_time()
            self.check_events()

            match self.player_controller_mode:
                case PLAYER_CONTROLLER_MODE.FLOATING_CAMERA:
                    self.camera.move()
                case PLAYER_CONTROLLER_MODE.FPS:
                    self.player_controller.move()
                case PLAYER_CONTROLLER_MODE.MENU:
                    pass
                case _:
                    raise NotImplementedError

            self.camera.update()
            self.player_controller.update()
            self.render()
            self.delta_time: int = self.clock.tick(settings.OpenGL.FPS_TARGET)
            self.delta_time_s: float = self.delta_time * MS_TO_SECOND

            self.frame_counter += 1

            self.camera_projection_has_changed = False

    def __del__(self) -> None:
        self.logger.info("Cleaning up Graphics Enging.")
        try:
            self.mesh.destroy()
        except AttributeError:
            self.logger.warning("Didn't have a mesh when getting destroyed.")
        pg.quit()

        self.logger.info("Cleanup is done, deleting logger now.")
        my_logger.cleanup(self.logger)

    def take_screenshot(self) -> None:
        screen: pg.Surface = pg.display.get_surface()
        screen_surf: pg.Surface = pygame.image.fromstring(
            self.ctx.screen.read(), screen.get_size(), "RGB", True
        )

        filename = dt.datetime.now(dt.timezone.utc).strftime(
            settings.Screenshots.NAME_FORMAT
        )
        pg.image.save(
            screen_surf, os.path.join(settings.Folders.RECORDINGS_SCREENSHOTS, filename)
        )
        self.sound_screenshot.play()
