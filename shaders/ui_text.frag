
#version 330 core

in vec2 frag_texcoord;

out vec4 out_color;

uniform sampler2D text_texture;
uniform vec3 text_color;

void main() {
    float alpha = texture(text_texture, frag_texcoord).r;
    out_color = vec4(text_color, alpha);
}
