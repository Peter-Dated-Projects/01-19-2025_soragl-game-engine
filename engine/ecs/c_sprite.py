import pygame

import engine.context as ctx
from engine.io import resourcemanager
from engine.system import ecs


# ======================================================================== #
# Sprite
# ======================================================================== #


class SpriteComponent(ecs.Component):
    def __init__(
        self, image: pygame.Surface = None, filepath: str = None, rm_uuid: str = None
    ):
        super().__init__(SpriteComponent.__name__)
        self._image = (
            image if image is not None else ctx.CTX_RESOURCE_MANAGER.load(filepath)
        )
        self._filepath = filepath
        self._rm_uuid = rm_uuid if rm_uuid is not None else filepath
        self._rect = self._image.get_rect()

        # optional spritesheet
        self._spritesheet = None

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def update(self):
        pass

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
# Sprite Renderer Component
# ======================================================================== #


class SpriteRendererComponent(ecs.Component):
    def __init__(self, target: int = None):
        super().__init__(SpriteRendererComponent.__name__)
        self._target = target
        self._offset = pygame.Vector2()

    def __post_init__(self):
        if self._target is not None:
            self._target_comp = self._entity.get_component_by_id(self._target._uuid)
        else:
            self._target_comp = self._entity.get_component(SpriteComponent)

    # ------------------------------------------------------------------------ #
    # component logic
    # ------------------------------------------------------------------------ #

    def update(self):
        ctx.W_SURFACE.blit(
            self._target_comp.get_image(), self._entity._position + self._offset
        )
