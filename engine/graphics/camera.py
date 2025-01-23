import pygame

import engine.context as ctx
from engine.physics import entity

# ======================================================================== #
# Camera
# ======================================================================== #


class BaseCamera(entity.Entity):
    def __init__(self, render_distance: int, viewbox: pygame.Rect):
        super().__init__()

        self._render_distance = render_distance
        self._viewbox = viewbox


# ======================================================================== #
# 2D Camera
# ======================================================================== #


class Camera2D(BaseCamera):
    def __init__(self, render_distance: int, viewbox: pygame.Rect):
        super().__init__(render_distance, viewbox)

        self._chunk_pos = (0, 0)

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def generate_visible_chunks(self):
        self._chunk_pos = (
            self._position.x // ctx.DEFAULT_CHUNK_PIXEL_WIDTH,
            self._position.y // ctx.DEFAULT_CHUNK_PIXEL_HEIGHT,
        )
        # generate visible chunks
        for x in range(-self._render_distance, self._render_distance):
            for y in range(-self._render_distance, self._render_distance):
                yield (x + self._chunk_pos[0], y + self._chunk_pos[1])


# ======================================================================== #
# 3D Camera
# ======================================================================== #


class Camera3D(BaseCamera):
    def __init__(self, render_distance: int, viewbox: pygame.Rect):
        super().__init__(render_distance, viewbox)


# ======================================================================== #
# Camera Utils
# ======================================================================== #
