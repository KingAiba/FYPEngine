#version 330 core

in vec3 spriteColor;
in vec2 TexCoords;
//in float TexID;

uniform sampler2D Texture;

out vec4 color;

void main()
{
    //int index = int(TexID);
    color = vec4(spriteColor, 1.0) * texture(Texture, TexCoords);
}
