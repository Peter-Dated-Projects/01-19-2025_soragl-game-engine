import os
import sys
import platform
import math

if not os.environ.get("PYTHONHASHSEED"):
    os.environ["PYTHONHASHSEED"] = "13"

    import subprocess

    subprocess.run([sys.executable] + sys.argv)
    sys.exit()

# ======================================================================== #
# setup
# ======================================================================== #

import pygame

import engine.context as ctx

from engine.ecs import c_task
from engine.ecs import c_process
from engine.ecs import c_sprite
from engine.ecs import c_particle_handler

from engine.system import ecs
from engine.system import log
from engine.system import signal
from engine.system import animation

from engine.graphics import spritesheet

from engine.io import resourcemanager
from engine.io import inputhandler

from engine.physics import entity


ctx.WINDOW_WIDTH = 1280
ctx.WINDOW_HEIGHT = 720
ctx.WINDOW_TITLE = "Paint Gun Rogue-Lite"
ctx.WINDOW_FPS = 60
ctx.WINDOW_ICON = None
ctx.BACKGROUND_COLOR = (255, 247, 225)

# ctx.FRAMEBUFFER_WIDTH = 1280 // 3
# ctx.FRAMEBUFFER_HEIGHT = 720 // 3
ctx.FRAMEBUFFER_FLAGS = pygame.SRCALPHA
ctx.FRAMEBUFFER_BIT_DEPTH = 32

ctx.init()

# ======================================================================== #
# loading resources
# ======================================================================== #


# ------------------------------------------------------------------------ #
# testing zone

# test - loading images
image1 = ctx.CTX_RESOURCE_MANAGER.load("assets/entities/archer/idle.png")
image2 = ctx.CTX_RESOURCE_MANAGER.load("assets/entities/archer/walk.png")

# test - creating spritesheet
s1 = spritesheet.SpriteSheet.from_image(
    "assets/entities/archer/idle.png",
    spritesheet.SpriteSheet.create_meta(
        source="assets/entities/archer/idle.png", uniform=True, uwidth=100, uheight=100
    ),
)
s2 = spritesheet.SpriteSheet.from_image_array(
    [
        c_sprite.SpriteComponent(image2, "assets/entities/archer/walk.png"),
        c_sprite.SpriteComponent(image2, "assets/entities/archer/walk.png"),
    ]
)

# test - creating entity, adding component, rendering using task component!
e1 = ctx.CTX_WORLD.add_entity(entity.Entity())
e1spr = e1.add_component(
    c_sprite.SpriteComponent(filepath="assets/entities/arrow/32xarrow.png")
)
e1.add_component(c_sprite.SpriteRendererComponent(e1spr))
e1._position = pygame.Vector2(100, 100)
e1._zlayer = 2


def draw_image():
    ctx.W_FRAMEBUFFER.blit(image1, (100, 100))
    ctx.W_FRAMEBUFFER.blit(s1._image, (200, 200))

    # render sprites from spritesheet with spriterendereraspect
    for i in range(len(s1._sprites)):
        ctx.W_FRAMEBUFFER.blit(s1._sprites[i].get_image(), (300 + 30, 300 + 100 * i))

    # render s2
    for i in range(len(s2._sprites)):
        ctx.W_FRAMEBUFFER.blit(s2._sprites[i].get_image(), (300, 300 + 100 * i))

    ctx.CTX_SIGNAL_HANDLER.emit_signal(
        "draw_signal",
        (
            int(127 * math.sin(ctx.RUN_TIME) + 127),
            int(127 * math.cos(ctx.RUN_TIME) + 127),
            int(127 * math.sin(ctx.RUN_TIME + ctx.RUN_TIME * 0.5) + 127),
        ),
    )


def draw_signal(color):
    pygame.draw.rect(ctx.W_FRAMEBUFFER, color, (100, 200, 100, 100))


# test - add component using entity built in function
t1 = e1.add_component(c_task.TaskComponent("draw_image", draw_image))


# test - signal handler
ctx.CTX_SIGNAL_HANDLER.register_signal("draw_signal", [tuple])
ctx.CTX_SIGNAL_HANDLER.register_receiver("draw_signal", draw_signal)


# test - particle handler
e3 = ctx.CTX_WORLD.add_entity(entity.Entity())
e3._zlayer = -1
ph1 = e3.add_component(
    c_particle_handler.ParticleHandlerComponent(updates_per_second=10)
)

# ctx.CTX_SIGNAL_HANDLER.register_receiver(
#     "draw_signal", lambda color: print(e3._position)
# )

e3._position += pygame.Vector2(300, 100)

# ======================================================================== #
# run game
# ======================================================================== #


ctx.run()
