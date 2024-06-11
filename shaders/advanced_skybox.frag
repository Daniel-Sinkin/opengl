#version 330 core

out vec4 fragColor;

in vec4 clipCoords;

uniform samplerCube u_texture_skybox;
uniform mat4 m_invProjView;
uniform bool menuOpen;

void main() {
    if(menuOpen) {
        vec2 fragCoord = gl_FragCoord.xy;
        float screenWidth = 1600.0;
        float leftBoundary = 0.2 * screenWidth;
        if (fragCoord.x < leftBoundary) {
            discard;
        }
    }


    vec4 worldCoords = m_invProjView * clipCoords;
    vec3 texCubeCoord = normalize(worldCoords.xyz / worldCoords.w);
    fragColor = texture(u_texture_skybox, texCubeCoord);
}