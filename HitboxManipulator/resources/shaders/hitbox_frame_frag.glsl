#version 330

uniform sampler2D checkerBoard;
uniform sampler2D hitboxFramebuffer;

uniform vec4 borderColour;

uniform vec2 checkerUV;
uniform vec2 shift;

in vec2 frag_uv;

out vec4 fragColour;

void main(){
    vec4 checkerBoardColour = texture(checkerBoard, shift/32.0 + checkerUV*frag_uv - 0.5);
    vec4 fboColour = texture(hitboxFramebuffer, frag_uv + 0.5);
    fragColour = vec4(fboColour.rgb * fboColour.a + checkerBoardColour.rgb * (1.0 - fboColour.a), 1.0);
}