import time
import pygame
import numpy as np

import glm
import moderngl as mgl

from engine.system import signal
from engine.system import gamestate

from engine.graphics import camera

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

    # vertices
    vertices = [
        # point 0
        (1.0, 1.0, 1.0),
        # point 1
        (-1.0, 1.0, 1.0),
        # point 2
        (-1.0, -1.0, 1.0),
        # point 3
        (1.0, -1.0, 1.0),
        # point 4
        (1.0, 1.0, -1.0),
        # point 5
        (-1.0, 1.0, -1.0),
        # point 6
        (-1.0, -1.0, -1.0),
        # point 7
        (1.0, -1.0, -1.0),
    ]
    indices = [
        # front face
        (0, 1, 2),
        (0, 2, 3),
        # back face
        (4, 5, 6),
        (4, 6, 7),
        # left face
        (4, 0, 3),
        (4, 3, 7),
        # right face
        (1, 5, 6),
        (1, 6, 2),
        # top face
        (3, 2, 6),
        (3, 6, 7),
        # bottom face
        (4, 5, 1),
        (4, 1, 0),
    ]
    texcoords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    texcoord_indices = [
        # front face
        (0, 1, 2),
        (0, 2, 3),
        # back face
        (0, 1, 2),
        (0, 2, 3),
        # left face
        (0, 1, 2),
        (0, 2, 3),
        # right face
        (0, 1, 2),
        (0, 2, 3),
        # top face
        (0, 1, 2),
        (0, 2, 3),
        # bottom face
        (0, 1, 2),
        (0, 2, 3),
    ]

    v_data = np.array([vertices[i] for tri in indices for i in tri], dtype=np.float32)
    t_data = np.array(
        [texcoords[i] for tri in texcoord_indices for i in tri], dtype=np.float32
    )
    complete_vertex_data = np.hstack((v_data, t_data))

    # shader
    vshader_code = open("assets/shaders/default-vertex.glsl").read()
    fshader_code = open("assets/shaders/default-fragment.glsl").read()
    shader_program = consts.MGL_CONTEXT.program(
        vertex_shader=vshader_code, fragment_shader=fshader_code
    )

    # vao + vbo + ibo + attribs
    vbo = consts.MGL_CONTEXT.buffer(complete_vertex_data)
    vao = consts.MGL_CONTEXT.vertex_array(
        shader_program, [(vbo, "3f 2f", "in_position", "in_texcoords")]
    )

    _3dcam = camera.Camera3D(
        5,
        fov=45,
        near=0.1,
        far=1000,
        position=glm.vec3(2, 2, -3),
        forward=-glm.normalize(glm.vec3(2, 2, -3)),
    )
    m_model = glm.mat4()

    # shader
    shader_program["m_proj"].write(_3dcam._projection)
    shader_program["m_view"].write(_3dcam._view)
    shader_program["m_model"].write(m_model)

    # texture
    texture = consts.MGL_CONTEXT.texture(
        size=(consts.FRAMEBUFFER_WIDTH, consts.FRAMEBUFFER_HEIGHT),
        components=4,
        data=pygame.image.tostring(consts.W_FRAMEBUFFER, "RGBA"),
    )
    shader_program["tex"] = 0
    texture.use()

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

        # rotate the model matrix
        m_model = glm.rotate(m_model, consts.DELTA_TIME, glm.vec3(0, 1, 0))
        shader_program["m_model"].write(m_model)

        texture = consts.MGL_CONTEXT.texture(
            size=(consts.FRAMEBUFFER_WIDTH, consts.FRAMEBUFFER_HEIGHT),
            components=4,
            data=pygame.image.tostring(consts.W_FRAMEBUFFER, "RGBA", flipped=True),
        )
        texture.use()
        vao.render()

        # update window
        pygame.display.flip()
        consts.W_CLOCK.tick(consts.WINDOW_FPS)

    # cleaning
    vao.release()
    vbo.release()
    shader_program.release()

    pygame.quit()


def stop():
    # stop game
    consts.RUNNING = False
