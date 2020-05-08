#version 330 core
layout (location = 0) in vec4 vertex;

out vec2 TexCoords;
out vec4 ParticleColor;

uniform mat4 projection;
uniform float Scale;
uniform vec2 offset;
uniform vec4 color;

void main()
{
    TexCoords = vertex.zw;
    ParticleColor = color;
    gl_Position = projection * vec4((vertex.xy * Scale)+ offset, 0.0, 1.0);
}