import os
import sys
import platform

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

from engine.system import ecs
from engine.system import signal
from engine.system import animation

from engine.ecs import c_task
from engine.ecs import c_process


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


def draw_image():
    ctx.W_SURFACE.blit(image, (100, 100))
    print("drawing")


t1 = c_task.Task("draw_image", draw_image)
ctx.CTX_ECS_HANDLER.add_component(t1)

# ======================================================================== #
# run game
# ======================================================================== #


ctx.run()
