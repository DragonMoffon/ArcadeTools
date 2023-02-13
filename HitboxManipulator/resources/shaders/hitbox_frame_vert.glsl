#version 330

uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

in vec2 in_uv;

uniform vec2 pos;
uniform vec2 size;

out vec2 frag_uv;

void main(){
    gl_Position = window.projection * window.view * vec4(pos + in_uv*size, 0, 1);
    frag_uv = in_uv - 0.5;
}