#version 330 core

layout(location = 0) out vec4 color;

uniform sampler2D tex;

in vec2 f_uv;


void main() {
    color = texture(tex, f_uv);
    // color = vec4(vec3(f_uv, 0.0), 1.0);
}