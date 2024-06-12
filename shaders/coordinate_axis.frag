
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
