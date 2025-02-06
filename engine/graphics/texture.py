import pygame

import engine.context as ctx
import engine.constants as consts

# =============================================================================
# Texture
# =============================================================================


class Texture:
    # some static version of textures
    CACHE = {}

    @classmethod
    def get_texture(cls, path: str):
        if path in cls.CACHE:
            return cls.CACHE[path]

        # create texture
        texture = cls(path=path)
        cls.CACHE[path] = texture

        return texture

    @classmethod
    def __on_clean__(self):
        for texture in self.CACHE.values():
            texture.clean()

    @classmethod
    def is_cached(self, texture: "Texture"):
        return texture in self.CACHE.values()

    # ------------------------------------------------------------------------ #

    def __init__(self, path: str = None, raw_image: pygame.Surface = None):
        self._path = path
        self._raw_image = raw_image
        self._texture = None

        self._width = 0
        self._height = 0
        self._components = 0

        self.__create(filepath=self._path is not None)

    def __create(self, filepath: bool = False):
        # check if valid string
        if self._path is not None and not self._path.split(".")[-1] in [
            "png",
            "jpg",
            "jpeg",
        ]:
            print(__file__, "Invalid texture file")
            ctx.stop()

        # retrieve data
        if self._path is not None:
            self._raw_image = consts.CTX_RESOURCE_MANAGER.load(self._path)
        self._width, self._height = self._raw_image.get_size()
        self._components = self._raw_image.get_bytesize()

        # create texture object
        self._texture = consts.MGL_CONTEXT.texture(
            size=(self._width, self._height),
            components=self._components,
            data=pygame.image.tostring(self._raw_image, "RGBA", False),
        )

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def clean(self):
        self._texture.release()

    def use(self):
        self._texture.use()

    # ------------------------------------------------------------------------ #
    # special functions
    # ------------------------------------------------------------------------ #

    def __call__(self):
        return self._texture
