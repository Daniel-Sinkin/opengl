
#version 330 core

in vec3 fragColor;

out vec4 outColor;

void main() {
    vec2 fragCoord = gl_FragCoord.xy;

    outColor = vec4(fragColor, 1.0);
}
