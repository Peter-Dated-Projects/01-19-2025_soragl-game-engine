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

image = ctx.CTX_RESOURCE_MANAGER.load("assets/entities/archer/idle.png")

s1 = spritesheet.load_spritesheet("assets/entities/archer/idle.png")


def draw_image():
    ctx.W_SURFACE.blit(image, (100, 100))
    ctx.W_SURFACE.blit(s1.image, (200, 200))
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


t1 = c_task.Task("draw_image", draw_image)
ctx.CTX_ECS_HANDLER.add_component(t1)

ctx.CTX_SIGNAL_HANDLER.register_signal("draw_signal", [tuple])
ctx.CTX_SIGNAL_HANDLER.register_receiver("draw_signal", draw_signal)

# ======================================================================== #
# run game
# ======================================================================== #


ctx.run()
