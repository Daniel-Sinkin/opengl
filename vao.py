from moderngl import Buffer, Context, Program, VertexArray

from shader_program import ShaderProgram
from vbo import VBOHandler, VertexBufferObject


class VertexArrayObject:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.vbo = VBOHandler(ctx)
        self.program = ShaderProgram(ctx)
        self.vao_map: dict[str, VertexArray] = {
            k: self.get_vao(program=self.program.programs["default"], vbo=vbo)
            for k, vbo in self.vbo.vbo_map.items()
        }

    def get_vao(self, program: Program, vbo: VertexBufferObject) -> VertexArray:
        return self.ctx.vertex_array(
            program, [(vbo.vbo, vbo.buffer_format, *vbo.attributes)]
        )

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
