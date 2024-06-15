from . import *

""""""

import typing

from .texture import TextureHandler
from .vao import VertexArrayObject

if typing.TYPE_CHECKING:
    from .graphics_engine import GraphicsEngine


class Mesh:
    def __init__(self, app: "GraphicsEngine"):
        self.app: GraphicsEngine = app
        self.vao = VertexArrayObject(app.ctx)
        self.texture = TextureHandler(app)

    def destroy(self) -> None:
        self.vao.destroy
        self.texture.destroy()
