import pygame

from engine.io import resourcemanager

from engine.system import ecs


# ======================================================================== #
# Sprite
# ======================================================================== #


class Sprite(ecs.Component):
    def __init__(self, image: pygame.Surface, rm_uuid: str):
        super().__init__(self.__class__.__name__)
        self._image = image
        self._rm_uuid = rm_uuid

        self._spritesheet = None

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def get_image(self):
        return self._image

    def get_rm_uuid(self):
        return self._rm_uuid

    def get_source_image(self):
        # sprite rm_uuids are stored as: f"{image path}||{frame number}"
        return resourcemanager.load(self._rm_uuid.split("||")[0])

    def get_rect(self):
        return self._rect

    # ------------------------------------------------------------------------ #
    # special methods
    # ------------------------------------------------------------------------ #

    def __str__(self):
        return f"Sprite(name={self._name})"


# ======================================================================== #
# Sprite Renderer Aspect
# ======================================================================== #


class SpriteRendererAspect(ecs.Aspect):
    def __init__(self, sprite: Sprite):
        super().__init__(SpriteRendererAspect.__name__, [Sprite])

    # ------------------------------------------------------------------------ #
    # aspect logic
    # ------------------------------------------------------------------------ #

    def update(self, sprite: Sprite):
        # figure out later
        pass
