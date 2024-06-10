import sys
import typing

import moderngl as mgl
import pygame as pg

from camera import Camera
from light import Light
from mesh import Mesh
from model import Cube


class GraphicsEngine:
    def __init__(self, win_size: tuple[float, float] = (1600.0, 900.0)):
        pg.init()

        self.WIN_SIZE: tuple[float, float] = win_size

        # OpenGL setup
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        # OpenGL Context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Locks mouse into window
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx: mgl.Context = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Cube(self)

    def check_events(self) -> None:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT | pg.MOUSEBUTTONDOWN:
                    self.mesh.destroy()
                    pg.quit()
                    sys.exit()
                case pg.MOUSEMOTION:
                    mouse_rel = typing.cast(tuple[int, int], event.rel)
                    if mouse_rel != (0, 0):
                        self.camera.rotate(*mouse_rel)

                        pg.mouse.set_pos((self.WIN_SIZE[0] // 2, self.WIN_SIZE[1] // 2))
                        # Flushes the mouse position buffer
                        pg.mouse.get_rel()

    def render(self) -> None:
        self.ctx.clear(color=(0.08, 0.16, 0.18))

        self.scene.render()

        pg.display.flip()

    def get_time(self) -> None:
        self.time = pg.time.get_ticks() * 0.001

    def run(self) -> typing.NoReturn:
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60.0)


def main() -> typing.NoReturn:
    app = GraphicsEngine()
    app.run()


if __name__ == "__main__":
    main()
