#version 330 core

layout(location = 0) out vec4 color;

uniform sampler2D[10] u_textures;

in vec2 f_uv;
in float f_tex;


void main() {
    color = texture(u_textures[int(f_tex)], f_uv);
}
