import moderngl as mgl
from moderngl import Context, Program


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
            ]
        }

        self.programs["coordinate_axis"] = self.ctx.program(
            vertex_shader="""
            #version 330 core

            layout(location = 0) in vec3 in_position;
            layout(location = 1) in vec3 in_color;

            out vec3 fragColor;

            uniform mat4 m_view;
            uniform mat4 m_proj;
            uniform mat4 m_model;

            void main() {
                gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                fragColor = in_color;
            }
            """,
            fragment_shader="""
            #version 330 core

            in vec3 fragColor;

            out vec4 outColor;

            void main() {
                vec2 fragCoord = gl_FragCoord.xy;
                float screenWidth = 1600.0;
                float leftBoundary = 0.2 * screenWidth;
                if (fragCoord.x < leftBoundary) {
                    discard;
                }
            
                outColor = vec4(fragColor, 1.0);
            }
            """,
        )

    def get_shader_program(self, shader_name) -> Program:
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program: Program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program

    def destroy(self) -> None:
        for program in self.programs.values():
            program.release()
