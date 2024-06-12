
#version 330 core

in vec4 in_position;
in vec2 in_texcoord_0;

out vec2 frag_texcoord;

void main() {
    gl_Position = in_position;
    frag_texcoord = in_texcoord_0;
}
