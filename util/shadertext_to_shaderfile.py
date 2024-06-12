"""
When copying shader templates they are often written as python strings, this script gets those
as input and creates the corresponding file.
"""

import os

name = "coordinate_axis"

vertex_shader = """
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
"""
fragment_shader = """
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
"""


def create_shaders() -> None:
    with open(f"./shaders/{name}.vert", "w") as file:
        file.write(vertex_shader)
    print(f"Created {name}.vert")

    with open(f"./shaders/{name}.frag", "w") as file:
        file.write(fragment_shader)
    print(f"Created {name}.frag")


if __name__ == "__main__":
    create_shaders()
