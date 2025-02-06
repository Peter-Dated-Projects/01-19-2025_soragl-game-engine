import time
import pygame
import numpy as np

import glm
import moderngl as mgl

import pywavefront

from engine.system import signal
from engine.system import gamestate

from engine.graphics import buffer
from engine.graphics import camera
from engine.graphics import shader
from engine.graphics import texture

from engine.physics import entity

from engine.io import resourcemanager
from engine.io import inputhandler

from OpenGL.GL import *
from OpenGL.GLUT import *

import engine.constants as consts


# ======================================================================== #
# init
# ======================================================================== #


def init():
    pygame.init()

    # ------------------------------------------------------------------------ #
    # opengl setup
    # ------------------------------------------------------------------------ #
    print("Initializing OpenGL Context...")

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)

    # ------------------------------------------------------------------------ #
    # pygame window
    # ------------------------------------------------------------------------ #

    print("Initializing pygame window Context...")

    consts.W_SURFACE = pygame.display.set_mode(
        (consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT),
        consts.WINDOW_FLAGS,
        consts.WINDOW_BIT_DEPTH,
    )
    consts.MGL_CONTEXT = mgl.create_context()
    consts.W_CLOCK = pygame.time.Clock()
    consts.W_FRAMEBUFFER = pygame.Surface(
        (consts.FRAMEBUFFER_WIDTH, consts.FRAMEBUFFER_HEIGHT),
        consts.FRAMEBUFFER_FLAGS,
        consts.FRAMEBUFFER_BIT_DEPTH,
    ).convert_alpha()
    # set pygame window specs
    pygame.display.set_caption(consts.WINDOW_TITLE)
    if consts.WINDOW_ICON:
        pygame.display.set_icon(consts.WINDOW_ICON)

    # create objects
    consts.CTX_INPUT_HANDLER = inputhandler.InputHandler()
    consts.CTX_SIGNAL_HANDLER = signal.SignalHandler()
    consts.CTX_RESOURCE_MANAGER = resourcemanager.ResourceManager()

    consts.CTX_GAMESTATE_MANAGER = gamestate.GameStateManager()
    # update ecs handler
    consts.CTX_ECS_HANDLER = consts.CTX_GAMESTATE_MANAGER.get_current_ecs()

    # ------------------------------------------------------------------------ #
    # register signals
    # ------------------------------------------------------------------------ #

    consts.CTX_SIGNAL_HANDLER.register_signal("SORA_ENTITY_DEATH", [entity.Entity])


def run():
    # run game
    consts.RUNNING = True

    # begin the game loop
    consts.START_TIME = time.time()
    consts.END_TIME = consts.START_TIME
    consts.RUN_TIME = 0

    # ------------------------------------------------------------------------ #
    # testing

    # get opengl data
    print("OpenGL version:", glGetString(GL_VERSION).decode())
    print("GLSL version:", glGetString(GL_SHADING_LANGUAGE_VERSION).decode())

    consts.MGL_CONTEXT.enable(flags=mgl.DEPTH_TEST)
    glDepthFunc(GL_LESS)
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # ------------------------------------------------------------------------ #

    while consts.RUNNING:
        # ------------------------------------------------------------------------ #
        # time
        # ------------------------------------------------------------------------ #
        print(
            f"{consts.RUN_TIME:.5f} | ===================== START NEW LOOP ================================"
        )
        # calculate delta time
        consts.START_TIME = time.time()
        consts.DELTA_TIME = consts.START_TIME - consts.END_TIME
        consts.END_TIME = consts.START_TIME
        consts.RUN_TIME += consts.DELTA_TIME

        # ------------------------------------------------------------------------ #
        # events
        # ------------------------------------------------------------------------ #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                consts.RUNNING = False

            # window resize events
            if event.type == pygame.VIDEORESIZE:
                consts.WINDOW_WIDTH = event.w
                consts.WINDOW_HEIGHT = event.h

        # ------------------------------------------------------------------------ #
        # reset + clearing
        # ------------------------------------------------------------------------ #

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        consts.W_FRAMEBUFFER.fill(consts.BACKGROUND_COLOR)

        # ------------------------------------------------------------------------ #
        # updating
        # ------------------------------------------------------------------------ #

        # update game state
        consts.CTX_INPUT_HANDLER.update()
        consts.CTX_GAMESTATE_MANAGER.update()

        # update aspects
        consts.CTX_SIGNAL_HANDLER.handle()
        consts.W_SURFACE.blit(
            pygame.transform.scale(consts.W_FRAMEBUFFER, consts.W_SURFACE.get_size()),
            (0, 0),
        )

        # ------------------------------------------------------------------------ #
        # drawing
        # ------------------------------------------------------------------------ #

        # update window
        pygame.display.flip()
        consts.W_CLOCK.tick(consts.WINDOW_FPS)

    # ------------------------------------------------------------------------ #
    # final cleaning
    # ------------------------------------------------------------------------ #

    # clear up all game states
    consts.CTX_GAMESTATE_MANAGER.__on_clean__()
    # clean up textures
    texture.Texture.__on_clean__()

    pygame.quit()

    print("Game Stopped + Caches + Memory Cleaned")


def stop():
    # stop game
    consts.RUNNING = False
