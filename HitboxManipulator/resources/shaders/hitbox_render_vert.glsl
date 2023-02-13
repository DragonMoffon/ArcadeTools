#version 330

uniform vec2 shift;
uniform vec2 spriteSize;
uniform vec2 frameSize;
uniform float zoom;

in vec2 pos;

void main(){
    gl_Position = vec4((pos - shift) / (0.5 * zoom * frameSize) , 0.0, 1.0);

}