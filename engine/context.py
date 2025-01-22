import pygame
import engine
import time

from engine.system import signal
from engine.system import ecs

from engine.io import resourcemanager

# ======================================================================== #
# context
# ======================================================================== #

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

BACKGROUND_COLOR = (255, 0, 0)

# pygame objects
W_SURFACE = None
W_CLOCK = None

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


# ======================================================================== #
# init
# ======================================================================== #


def init():
    global CTX_SIGNAL_HANDLER
    global CTX_RESOURCE_MANAGER
    global CTX_ECS_HANDLER

    CTX_RESOURCE_MANAGER = resourcemanager.ResourceManager()
    CTX_SIGNAL_HANDLER = signal.SignalHandler()
    CTX_ECS_HANDLER = ecs.ECSHandler()

    print("Initializing pygame window Context...")

    # create window object
    global W_SURFACE, W_CLOCK

    W_SURFACE = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_FLAGS, WINDOW_BIT_DEPTH
    )
    W_CLOCK = pygame.time.Clock()

    # set pygame window specs
    pygame.display.set_caption(WINDOW_TITLE)
    if WINDOW_ICON:
        pygame.display.set_icon(WINDOW_ICON)


def run():
    # run game
    global RUNNING, START_TIME, END_TIME, DELTA_TIME
    RUNNING = True

    # begin the game loop
    while RUNNING:
        # calculate delta time
        START_TIME = time.time()
        DELTA_TIME = START_TIME - END_TIME
        END_TIME = START_TIME

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            # window resize events
            if event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH = event.w
                WINDOW_HEIGHT = event.h

        print(DELTA_TIME)

        # reset background
        W_SURFACE.fill(BACKGROUND_COLOR)

        # update aspects
        CTX_ECS_HANDLER.update()

        # update window
        pygame.display.flip()
        W_CLOCK.tick(WINDOW_FPS)


def stop():
    # stop game
    global RUNNING
    RUNNING = False
