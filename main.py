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
ctx.BACKGROUND_COLOR = (133, 193, 233)

ctx.init()

# ======================================================================== #
# loading resources
# ======================================================================== #

# loading aspects
ctx.CTX_ECS_HANDLER.add_aspect(c_task.TaskAspect())
ctx.CTX_ECS_HANDLER.add_aspect(c_process.ProcessAspect())


# ------------------------------------------------------------------------ #
# testing zone

# test - loading images
image = ctx.CTX_RESOURCE_MANAGER.load("assets/entities/archer/idle.png")

# test - creating spritesheet
s1 = spritesheet.SpriteSheet.from_image(
    "assets/entities/archer/idle.png",
    spritesheet.SpriteSheet.create_meta(
        source="assets/entities/archer/idle.png", uniform=True, uwidth=100, uheight=100
    ),
)

# test - creating entity, adding component, rendering using task component!
e1 = ctx.CTX_WORLD.add_entity(entity.Entity())


def draw_image():
    ctx.W_SURFACE.blit(image, (100, 100))
    ctx.W_SURFACE.blit(s1._image, (200, 200))
    print("drawing")

    ctx.CTX_SIGNAL_HANDLER.emit_signal(
        "draw_signal",
        (
            int(127 * math.sin(ctx.RUN_TIME) + 127),
            int(127 * math.cos(ctx.RUN_TIME) + 127),
            int(127 * math.sin(ctx.RUN_TIME + ctx.RUN_TIME * 0.5) + 127),
        ),
    )


def draw_signal(color):
    print("drawing signal")
    print(color)
    pygame.draw.rect(ctx.W_SURFACE, color, (100, 100, 100, 100))


# test - add component using entity built in function
t1 = e1.add_component(c_task.Task("draw_image", draw_image))
# test - add component using ecs handler
t2 = ctx.CTX_ECS_HANDLER.add_component(
    c_task.Task("log_update", lambda: print("updated from log update")), e1
)


# test - signal handler
ctx.CTX_SIGNAL_HANDLER.register_signal("draw_signal", [tuple])
ctx.CTX_SIGNAL_HANDLER.register_receiver("draw_signal", draw_signal)

# ======================================================================== #
# run game
# ======================================================================== #


ctx.run()
