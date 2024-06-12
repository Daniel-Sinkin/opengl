import pygame as pg

from . import settings


def setup_opengl(window_size: tuple[int, int]) -> pg.Surface:
    pg.init()

    # OpenGL setup
    pg.display.gl_set_attribute(
        pg.GL_CONTEXT_MAJOR_VERSION, settings.OpenGL.MAJOR_VERSION
    )
    pg.display.gl_set_attribute(
        pg.GL_CONTEXT_MINOR_VERSION, settings.OpenGL.MINOR_VERSION
    )
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    # OpenGL Context
    return pg.display.set_mode(window_size, flags=pg.OPENGL | pg.DOUBLEBUF)
