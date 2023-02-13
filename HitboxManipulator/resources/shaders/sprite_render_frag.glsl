#version 330

uniform int tex_id;

uniform sampler2D textureInfo;
uniform sampler2D textureAtlas;

in vec2 fragUV;

out vec4 fragColour;

void main()
{
    vec4 texInfo = texelFetch(textureInfo, ivec2(tex_id, 0), 0);
    fragColour = texture(textureAtlas, texInfo.xy + texInfo.zw*fragUV, 0);
    // fragColour = vec4(texInfo.xy + texInfo.zw*fragUV, 0.0, 1.0);
}