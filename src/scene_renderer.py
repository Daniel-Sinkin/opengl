import typing

from moderngl import Context, Framebuffer, Texture

from .mesh import Mesh
from .scene import Scene

if typing.TYPE_CHECKING:
    from graphics_engine import GraphicsEngine


class SceneRenderer:
    def __init__(self, app: "GraphicsEngine"):
        self.app: GraphicsEngine = app
        self.ctx: Context = app.ctx
        self.mesh: Mesh = app.mesh
        self.scene: Scene = app.scene

        self.depth_texture: Texture = self.mesh.texture.textures["depth_texture"]
        self.depth_fbo: Framebuffer = self.ctx.framebuffer(
            depth_attachment=self.depth_texture
        )

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def main_render(self):
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def render(self):
        # Maybe also have a fixed_update function for physics stuff
        self.scene.update()
        self.render_shadow()
        self.main_render()

    def destroy(self):
        self.depth_fbo.release()
