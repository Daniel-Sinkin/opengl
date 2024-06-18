from . import *

""""""

from .settings import Folders


class ShaderProgram:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.programs: dict[str, Program] = {
            k: self.get_shader_program(k)
            for k in [
                "default",
                "skybox",
                "advanced_skybox",
                "shadow_map",
                "quad",
                "coordinate_axis",
                "ui_text",
                "line",
                "collider",
            ]
        }

    def get_shader_program(self, shader_name) -> Program:
        with open(os.path.join(Folders.SHADERS, f"{shader_name}.vert")) as file:
            vertex_shader = file.read()

        with open(os.path.join(Folders.SHADERS, f"{shader_name}.frag")) as file:
            fragment_shader = file.read()

        program: Program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program

    def destroy(self) -> None:
        for program in self.programs.values():
            program.release()
