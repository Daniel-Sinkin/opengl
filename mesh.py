import typing

from texture import TextureHandler
from vao import VertexArrayObject

if typing.TYPE_CHECKING:
    from main import GraphicsEngine


class Mesh:
    # TODO: Check if we need the "..." around the forward declaration in python 3.12
    def __init__(self, app: "GraphicsEngine"):
        self.app: "GraphicsEngine" = app
        self.vao = VertexArrayObject(app.ctx)
        self.texture = TextureHandler(app)

    def destroy(self):
        self.vao.destroy
        self.texture.destroy()
