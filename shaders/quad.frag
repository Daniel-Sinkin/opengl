#version 330

out vec4 out_color;

uniform bool menuOpen;

void main() {
    if(menuOpen) {
        out_color = vec4(0.3, 0.3, 0.7, 1.0);
    } else {
        discard;
    }
}