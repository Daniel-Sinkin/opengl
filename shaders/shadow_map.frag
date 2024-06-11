#version 330 core

void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    float screenWidth = 1600.0;
    float leftBoundary = 0.2 * screenWidth;
    if (fragCoord.x < leftBoundary) {
        discard;
    }
}