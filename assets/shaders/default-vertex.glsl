#version 330 core

layout (location = 0) in vec3 in_position;
layout(location = 1) in vec2 in_texcoords;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec2 f_uv;

void main() {
    f_uv = in_texcoords;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}