#version 330 core
layout (location = 0) in vec4 aPos; // <vec2 position, vec2 texCoords>

out vec2 TexCoords;


uniform mat4 model;
uniform mat4 projection;
uniform vec2 FullGrid;
uniform vec2 CurrCoord;


void main()
{
    vec2 temp = aPos.zw;
    if(temp.x == 0 && temp.y == 0){
        temp.x = temp.x+((CurrCoord.x-1)/FullGrid.x);
        temp.y = temp.y+((CurrCoord.y-1)/FullGrid.y);
    }else if(temp.x == 1 && temp.y == 0){
        temp.x = (CurrCoord.x/FullGrid.x);
        temp.y = temp.y+((CurrCoord.y-1)/FullGrid.y);
    }else if(temp.x == 0 && temp.y == 1){
        temp.x = temp.x+((CurrCoord.x-1)/FullGrid.x);
        temp.y = (CurrCoord.y/FullGrid.y);
    }else if(temp.x == 1 && temp.y == 1){
        temp.x = (CurrCoord.x/FullGrid.x);
        temp.y = (CurrCoord.y/FullGrid.y);
    }


    TexCoords = temp;
    gl_Position = projection * model * vec4(aPos.xy, 0.0, 1.0);
}