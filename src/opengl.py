import pygame as pg

from .settings import Settings_OpenGL


def setup_opengl(window_size: tuple[int, int]) -> None:
    pg.init()

    # OpenGL setup
    pg.display.gl_set_attribute(
        pg.GL_CONTEXT_MAJOR_VERSION, Settings_OpenGL.MAJOR_VERSION
    )
    pg.display.gl_set_attribute(
        pg.GL_CONTEXT_MINOR_VERSION, Settings_OpenGL.MINOR_VERSION
    )
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    # OpenGL Context
    pg.display.set_mode(window_size, flags=pg.OPENGL | pg.DOUBLEBUF)

    # Locks mouse into window
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
