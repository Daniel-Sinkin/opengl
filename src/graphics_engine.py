import sys
import typing
from logging import Logger
from typing import Optional

import moderngl as mgl
import pygame as pg

from . import my_logger
from .camera import Camera
from .constants import SECOND_TO_MS
from .light import Light
from .mesh import Mesh
from .model import Cube
from .my_logger import setup
from .opengl import setup_opengl
from .scene import Scene
from .scene_renderer import SceneRenderer
from .settings import Colors, Settings_OpenGL


class GraphicsEngine:
    def __init__(self, win_size: Optional[tuple[int, int]] = None):
        self.window_size: tuple[int, int] = Settings_OpenGL.WINDOW_SIZE
        setup_opengl(window_size=self.window_size)

        self.ctx: mgl.Context = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

        self.logger: Logger = my_logger.setup("GraphicsEngine")

        self.is_running = True
        self.tick_counter = 0

    def check_events(self) -> None:
        for event in pg.event.get():
            match event.type:
                # TODO: Add keyboard inputs here
                case pg.QUIT | pg.MOUSEBUTTONDOWN:
                    self.is_running = False

                case pg.MOUSEMOTION:
                    mouse_rel: tuple[int, int] = typing.cast(tuple[int, int], event.rel)
                    if mouse_rel != (0, 0):
                        self.camera.rotate(*mouse_rel)

                        pg.mouse.set_pos(
                            (self.window_size[0] // 2, self.window_size[1] // 2)
                        )
                        # Flushes the mouse position buffer
                        pg.mouse.get_rel()

    def render(self) -> None:
        # This should always be covered
        self.ctx.clear(color=Colors.MISSING_TEXTURE)

        self.scene_renderer.render()

        pg.display.flip()

    def get_time(self) -> None:
        self.time = pg.time.get_ticks() * SECOND_TO_MS

    def run(self) -> None:
        while self.is_running:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time: int = self.clock.tick(60.0)

            self.tick_counter += 1

    def __del__(self) -> None:
        self.logger.info("Cleaning up Graphics Enging.")
        self.mesh.destroy()
        pg.quit()

        self.logger.info("Cleanup is done, deleting logger now.")
        my_logger.cleanup(self.logger)
