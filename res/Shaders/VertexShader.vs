#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 scale;
uniform mat4 rotate;
uniform mat4 translate;

//uniform mat4 model;
//uniform mat4 view;
uniform mat4 P;

out vec3 ourColor;
out vec2 TexCoord;

void main()
{
    gl_Position =  translate * rotate * scale * vec4(aPos, 1.0);
    ourColor = aColor;
    TexCoord = aTexCoord;
}