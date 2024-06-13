from . import *

""""""

from .shader_program import ShaderProgram
from .vbo import VBOHandler, VertexBufferObject

# TODO: Consider if we should make the vao map into a named tuple
# fmt: off
vao_tuples: list[tuple[str, str, str]] = [
#     VAO_NAME            PROGRAM_NAME        VBO_NAME
    ( "cube"            , "default"         , "cube"            ),
    ( "shadow_cube"     , "shadow_map"      , "cube"            ),
    ( "cat"             , "default"         , "cat"             ),
    ( "shadow_cat"      , "shadow_map"      , "cat"             ),
    ( "skybox"          , "skybox"          , "skybox"          ),
    ( "advanced_skybox" , "advanced_skybox" , "advanced_skybox" ),
    ( "quad"            , "quad"            , "quad"            ),
    ( "sphere"          , "default"         , "sphere"          ),
    ( "shadow_sphere"   , "shadow_map"      , "sphere"          ),
    ( "coordinate_axis" , "coordinate_axis" , "coordinate_axis" ),
    ( "cylinder"        , "default"         , "cylinder"        ),
    ( "shadow_cylinder" , "shadow_map"      , "cylinder"        ),
    ( "ui_text"         , "ui_text"         , "ui_text"         ),
    ( "line"             , "line"           , "line"            ),
]
# fmt: on


class VertexArrayObject:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.vbo = VBOHandler(ctx)
        self.program = ShaderProgram(ctx)

        self.vao_map: dict[str, VertexArray] = {
            vao_name: self.create_vao_from_vbo(
                self.program.programs[program_name], self.vbo.vbo_map[vbo_name]
            )
            for vao_name, program_name, vbo_name in vao_tuples
        }

    def create_vao_from_vbo(
        self, program: Program, vbo: VertexBufferObject
    ) -> VertexArray:
        return self.ctx.vertex_array(
            program, [(vbo.vbo, vbo.buffer_format, *vbo.attributes)], skip_errors=True
        )

    def destroy(self) -> None:
        self.vbo.destroy()
        self.program.destroy()
