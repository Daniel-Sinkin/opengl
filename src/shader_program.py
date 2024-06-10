import moderngl as mgl
from moderngl import Context, Program


class ShaderProgram:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.programs: dict[str, Program] = {
            k: self.get_program(k)
            for k in ["default", "skybox", "advanced_skybox", "shadow_map"]
        }

    def get_program(self, shader_program_name) -> Program:
        with open(f"shaders/{shader_program_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_program_name}.frag") as file:
            fragment_shader = file.read()

        program: Program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program

    def destroy(self) -> None:
        for program in self.programs.values():
            program.release()
