import os
import sys
import platform

# TODO - figure out what to do when I compile this program (because that'll be quite a problem)
if not os.environ.get("PYTHONHASHSEED"):
    os.environ["PYTHONHASHSEED"] = "13"

    import subprocess

    subprocess.run([sys.executable] + sys.argv)
    sys.exit()
    # os.execv(sys.executable, ['python'] + sys.argv)

import dill
import time
import pickle
import moderngl
import pygame

import math

from engine import io
from engine import utils
from engine import singleton

from engine.handler import signal
from engine.handler import world

from engine.physics import phandler
from engine.physics import gameobject

from engine.ui import ui

from engine.graphics import gl
from engine.graphics import animation
from engine.graphics import spritesheet

from engine.addon import tiles
from engine.addon import components
from engine.addon import physicscomponents

# ---------------------------- #
# create a window

pygame.init()

clock = pygame.time.Clock()

singleton.WIN_BACKGROUND = utils.hex_to_rgb("000000")
singleton.set_framebuffer_size_factor(3)
singleton.DEBUG = True
singleton.set_render_distance(4)
singleton.set_fps(60)

gl.GLContext.add_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
gl.GLContext.add_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
gl.GLContext.add_attribute(
    pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
)
gl.GLContext.add_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
gl.GLContext.create_context()

"""

When creating a world, adding components, and creating gameobjects, here is the general order of 
steps you should follow to ensure things start up correctly:

1. Create the world (or load up a world)
2. Add aspects to the world
3. Add physics objects to the world
4. Create gameobjects
5. Add components to the gameobjects

It's pretty simple, but it's important to follow this order to ensure that everything is set up

Have fun!

"""

# -------------------------------------------------------------------------- #
# testing


# -------------------------------------------------------------------------- #

singleton.RUNNING = True
singleton.START_TIME = time.time()

while singleton.RUNNING:
    singleton.END_TIME = time.time()
    singleton.DELTA_TIME = singleton.END_TIME - singleton.START_TIME
    singleton.START_TIME = singleton.END_TIME

    # ---------------------------- #
    # update loop

    singleton.FRAMEBUFFER.fill(singleton.WIN_BACKGROUND)
    singleton.SCREENBUFFER.fill((0, 0, 0, 0))

    # TODO - include world rendering

    # ---------------------------- #
    # final rendering
    gl.GLContext.render_to_opengl_window(
        singleton.FRAMEBUFFER,
        singleton.DEFAULT_SHADER,
        singleton.FRAMEBUFFER_SHADER_QUAD,
        {"tex": 0, "time": singleton.ACTIVE_TIME},
    )
    gl.GLContext.render_to_opengl_window(
        singleton.SCREENBUFFER,
        singleton.DEFAULT_SCREEN_SHADER,
        singleton.SCREEN_SHADER_QUAD,
        {"tex": 0, "time": singleton.ACTIVE_TIME},
    )

    pygame.display.flip()

    # ---------------------------- #
    # update events
    singleton.system_update_function()

    # update signals
    signal.update_signals()
    time.sleep(
        utils.clamp(
            singleton.DESIRE_DELTA - singleton.DELTA_TIME, 0, singleton.DESIRE_DELTA
        )
    )

    # update statistics
    singleton.FRAME_COUNTER += 1
    singleton.ACTIVE_TIME += singleton.DELTA_TIME


# -------------------------------------------------------------------------- #
pygame.quit()
