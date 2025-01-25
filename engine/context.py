import pygame
import engine
import time

from engine.system import signal
from engine.system import ecs
from engine.system import gamestate

from engine.io import resourcemanager

# ======================================================================== #
# context
# ======================================================================== #

ENGINE_NAME = "SORAGL"

# all static data and objects
# singleton for main engine data

RUNNING = False

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Paint Gun Rogue-Lite"
WINDOW_FPS = 60
WINDOW_BIT_DEPTH = 32
WINDOW_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
WINDOW_ICON = "assets/icon.png"

FRAMEBUFFER_WIDTH = 1280
FRAMEBUFFER_HEIGHT = 720
FRAMEBUFFER_BIT_DEPTH = 32
FRAMEBUFFER_FLAGS = pygame.SRCALPHA

BACKGROUND_COLOR = (255, 0, 0)

# pygame objects
W_SURFACE = None
W_CLOCK = None
W_FRAMEBUFFER = None

# time
DELTA_TIME = 0
START_TIME = 0
END_TIME = 0

RUN_TIME = 0

# objects
CTX_WINDOW = None
CTX_ECS_HANDLER = None
CTX_SIGNAL_HANDLER = None
CTX_RESOURCE_MANAGER = None
CTX_GAMESTATE_MANAGER = None

# world constants
DEFAULT_CHUNK_PIXEL_WIDTH = 4096
DEFAULT_CHUNK_PIXEL_HEIGHT = 4096


# ======================================================================== #
# init
# ======================================================================== #


def init():

    # create window object
    global W_SURFACE, W_CLOCK, W_FRAMEBUFFER

    W_SURFACE = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_FLAGS, WINDOW_BIT_DEPTH
    )
    W_CLOCK = pygame.time.Clock()
    W_FRAMEBUFFER = pygame.Surface(
        (FRAMEBUFFER_WIDTH, FRAMEBUFFER_HEIGHT),
        FRAMEBUFFER_FLAGS,
        FRAMEBUFFER_BIT_DEPTH,
    ).convert_alpha()
    # set pygame window specs
    pygame.display.set_caption(WINDOW_TITLE)
    if WINDOW_ICON:
        pygame.display.set_icon(WINDOW_ICON)

    # create objects
    global CTX_SIGNAL_HANDLER
    global CTX_RESOURCE_MANAGER
    global CTX_GAMESTATE_MANAGER
    global CTX_ECS_HANDLER

    CTX_SIGNAL_HANDLER = signal.SignalHandler()
    CTX_RESOURCE_MANAGER = resourcemanager.ResourceManager()

    CTX_GAMESTATE_MANAGER = gamestate.GameStateManager()
    # update ecs handler
    CTX_ECS_HANDLER = CTX_GAMESTATE_MANAGER.get_current_ecs()

    print("Initializing pygame window Context...")


def run():
    # run game
    global RUNNING, START_TIME, END_TIME, DELTA_TIME, RUN_TIME
    RUNNING = True

    # begin the game loop
    START_TIME = time.time()
    END_TIME = START_TIME
    RUN_TIME = 0

    while RUNNING:
        # calculate delta time
        START_TIME = time.time()
        DELTA_TIME = START_TIME - END_TIME
        END_TIME = START_TIME
        RUN_TIME += DELTA_TIME

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            # window resize events
            if event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH = event.w
                WINDOW_HEIGHT = event.h

        # reset background
        W_FRAMEBUFFER.fill(BACKGROUND_COLOR)

        # update game state
        CTX_GAMESTATE_MANAGER.update()

        # update aspects
        CTX_SIGNAL_HANDLER.handle()
        W_SURFACE.blit(
            pygame.transform.scale(W_FRAMEBUFFER, W_SURFACE.get_size()), (0, 0)
        )
        # update window
        pygame.display.flip()
        W_CLOCK.tick(WINDOW_FPS)


def stop():
    # stop game
    global RUNNING
    RUNNING = False


# ======================================================================== #
# constants
# ======================================================================== #


class Constants:

    UP = pygame.Vector2(0, 1)
    DOWN = pygame.Vector2(0, -1)
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
