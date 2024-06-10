from moderngl import Buffer, Context, Program, VertexArray

from .shader_program import ShaderProgram
from .vbo import VBOHandler, VertexBufferObject


class VertexArrayObject:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.vbo = VBOHandler(ctx)
        self.program = ShaderProgram(ctx)

        self.vao_map: dict[str, VertexArray] = {
            "cube": self.get_vao(
                self.program.programs["default"], self.vbo.vbo_map["cube"]
            ),
            "shadow_cube": self.get_vao(
                self.program.programs["shadow_map"], self.vbo.vbo_map["cube"]
            ),
            "cat": self.get_vao(
                self.program.programs["default"], self.vbo.vbo_map["cat"]
            ),
            "shadow_cat": self.get_vao(
                self.program.programs["shadow_map"], self.vbo.vbo_map["cat"]
            ),
            "skybox": self.get_vao(
                self.program.programs["skybox"], self.vbo.vbo_map["skybox"]
            ),
            "advanced_skybox": self.get_vao(
                self.program.programs["advanced_skybox"],
                self.vbo.vbo_map["advanced_skybox"],
            ),
        }

    def get_vao(self, program: Program, vbo: VertexBufferObject) -> VertexArray:
        return self.ctx.vertex_array(
            program, [(vbo.vbo, vbo.buffer_format, *vbo.attributes)], skip_errors=True
        )

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
