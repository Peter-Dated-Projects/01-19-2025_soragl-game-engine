import numpy as np

import engine.context as ctx
import engine.constants as consts

from engine.graphics import texture


# ============================================================================= #
# Rendering Manifold
# ============================================================================= #


class RenderingManifold:
    def __init__(
        self,
        vao: "VAOObject" = None,
        tex_count: int = 10,
        tex_uniform_name: str = "u_textures",
    ):
        self._vao = vao
        self._textures = [[i + 1, None] for i in range(tex_count)]

        self._tex_count = tex_count
        self._tex_uniform_name = tex_uniform_name

        if not self._vao:
            return
        # set default variables into shader program
        self.write_uniform(
            self._tex_uniform_name,
            np.array([i + 1 for i in range(tex_count)], dtype="int32"),
        )

    def __on_clean__(self):
        if not self._vao:
            return

        # clean if vao exists
        self._vao.clean()
        for i, tex in self._textures:
            if not tex:
                continue
            if not texture.Texture.is_cached(tex):
                tex.clean()
        self._textures.clear()

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def handle(self):
        if not self._vao:
            return
        # stage 1: should have written required variables to shader
        # stage 2: use texture
        for i, tex in self._textures:
            if not tex:
                continue
            tex().use(location=i)

        # stage 3: render
        self._vao().render()

    def write_uniform(self, uniform_name: str, data):
        self._vao._shader_program[uniform_name].write(data)

    def set_uniform(self, uniform_name: str, data):
        self._vao._shader_program[uniform_name] = data

    def set_texture(self, key: int, texture: "TextureObject"):
        self._textures[key][1] = texture

    def remove_texture(self, key: int):
        self._textures.pop(key)

    # ------------------------------------------------------------------------ #
    # special functions
    # ------------------------------------------------------------------------ #

    def get_texture_uniform_var(self, index: int):
        return f"texture{index}"


# ============================================================================= #
# VAO
# ============================================================================= #


class VAOObject:
    def __init__(self, shader_program: "ShaderProgram", attributes: "List[Tuple]"):
        self._uuid = 0
        self._shader_program = shader_program
        self._attributes = attributes

        # create vao
        self._vao = consts.MGL_CONTEXT.vertex_array(
            self._shader_program(), self._attributes
        )

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def clean(self):
        self._vao.release()

    # ------------------------------------------------------------------------ #
    # special functions
    # ------------------------------------------------------------------------ #

    def __call__(self):
        return self._vao


# ============================================================================= #
# GL Buffer Object
# ============================================================================= #


class GLBufferObject:
    def __init__(self, buffer_data: list, reserve_size: int = 0, dynamic: bool = False):
        self._buffer_data = buffer_data
        self._reserver_size = reserve_size
        self._dynamic = dynamic

        # create buffer
        self._glbuffer = consts.MGL_CONTEXT.buffer(
            self._buffer_data, reserve=self._reserver_size, dynamic=self._dynamic
        )

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def clean(self):
        self._glbuffer.release()

    # ------------------------------------------------------------------------ #
    # special functions
    # ------------------------------------------------------------------------ #

    def __call__(self):
        return self._glbuffer
