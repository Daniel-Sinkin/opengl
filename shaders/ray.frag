
#version 330 core

in vec3 fragColor;
out vec4 out_color;

void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    out_color = vec4(fragColor, 1.0);
}
