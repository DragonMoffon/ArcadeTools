#version 330

uniform sampler2D checkerBoard;
uniform sampler2D hitboxFramebuffer;

uniform vec4 borderColour;

uniform vec2 checkerUV;
uniform vec2 shift;

in vec2 frag_uv;

out vec4 fragColour;

void main(){
    vec4 checkerBoardColour = texture(checkerBoard, shift + checkerUV*frag_uv);
    vec4 fboColour = texture(hitboxFramebuffer, frag_uv);
    fragColour.rgb = fboColour.rgb * fboColour.a + checkerBoardColour.rgb * (1 - fboColour.a);
    fragColour.a = 1.0;
}