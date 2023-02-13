#version 330

uniform vec2 shift;
uniform vec2 spriteSize;
uniform vec2 frameSize;
uniform float zoom;

in vec2 vertUV;
out vec2 fragUV;

void main()
{
    gl_Position = vec4(((vertUV - vec2(0.5)) * spriteSize - shift) / (zoom * frameSize * 0.5), 0.0, 1.0) ;
    fragUV = vertUV;
}

