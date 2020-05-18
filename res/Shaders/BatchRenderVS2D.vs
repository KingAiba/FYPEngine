#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec3 inColor;
layout (location = 2) in vec2 inTexCoords;
layout (location = 3) in float inTexID;

uniform mat4 projection;

out vec3 spriteColor;
out vec2 TexCoords;
//out float TexID;

void main()
{
    spriteColor = inColor;
    TexCoords = inTexCoords;
    //TexID = inTexID;
    gl_Position = projection * vec4(aPos, 0.0, 1.0);
}
