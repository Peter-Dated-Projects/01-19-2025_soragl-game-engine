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
from engine.physics import interact
from engine.physics.ecs import c_AABB

ctx.WINDOW_WIDTH = 1280
ctx.WINDOW_HEIGHT = 720
ctx.WINDOW_TITLE = "Paint Gun Rogue-Lite"
ctx.WINDOW_FPS = 60
ctx.WINDOW_ICON = None
ctx.BACKGROUND_COLOR = (255, 247, 225)

ctx.FRAMEBUFFER_WIDTH = 1280 // 2
ctx.FRAMEBUFFER_HEIGHT = 720 // 2
ctx.FRAMEBUFFER_FLAGS = pygame.SRCALPHA
ctx.FRAMEBUFFER_BIT_DEPTH = 32

ctx.DEBUG_MODE = True

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
e1spr._extra["offset"] = pygame.Vector2(50, 50)
e1.add_component(c_sprite.SpriteRendererComponent(e1spr))
e1._position = pygame.Vector2(100, 100)
e1._zlayer = 2


def draw_image():
    # ctx.W_FRAMEBUFFER.blit(image1, (100, 100))
    # ctx.W_FRAMEBUFFER.blit(s1._image, (200, 200))

    # # render sprites from spritesheet with spriterendereraspect
    # for i in range(len(s1._sprites)):
    #     ctx.W_FRAMEBUFFER.blit(s1._sprites[i].get_image(), (300 + 30, 300 + 100 * i))

    # # render s2
    # for i in range(len(s2._sprites)):
    #     ctx.W_FRAMEBUFFER.blit(s2._sprites[i].get_image(), (300, 300 + 100 * i))

    # print(e1._components)

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
e3._position += pygame.Vector2(300, 100)


# test -- load animation
reg1 = animation.Animation.from_json(
    "assets/entities/archer/walk_animation.json"
).get_register()
reg2 = animation.Animation.from_json(
    "assets/entities/archer/idle_animation.json"
).get_register()
reg3 = animation.Animation.from_array(
    [
        c_sprite.SpriteComponent(image2, "assets/entities/archer/walk.png"),
        c_sprite.SpriteComponent(image2, "assets/entities/archer/walk.png"),
    ]
).get_register()
reg4 = animation.Animation.from_array(s1._sprites).get_register()

e4 = ctx.CTX_WORLD.add_entity(entity.Entity())
e4.add_component(
    animation.AnimatedSpriteComponent(
        animation.Animation.from_json("assets/entities/archer/walk_animation.json")
    )
)
e4.add_component(c_sprite.SpriteComponent())
e4.add_component(c_sprite.SpriteRendererComponent())
e4._position += pygame.Vector2(300, 100)


def draw_animation():
    reg1.update()
    ctx.W_FRAMEBUFFER.blit(reg1.get_current_sprite().get_image(), (100, 100))


e3.add_component(c_task.TaskComponent("draw_animation", draw_animation))

# test - physics
eleft = ctx.CTX_WORLD.add_entity(entity.Entity())
eright = ctx.CTX_WORLD.add_entity(entity.Entity())

eleft.add_component(c_AABB.AABBColliderComponent(20, 20))
eleft.add_component(c_sprite.SpriteComponent())
eleft.add_component(
    animation.AnimatedSpriteComponent(
        animation.Animation.from_json("assets/entities/archer/idle_animation.json")
    )
)
eleft.add_component(c_sprite.SpriteRendererComponent())
eleft.add_component(
    interact.InteractionFieldComponent(collision_mask=0b00000001)
)._velocity.x = 40

eright.add_component(c_AABB.AABBColliderComponent(20, 20))
eright.add_component(c_sprite.SpriteComponent())
eright.add_component(
    animation.AnimatedSpriteComponent(
        animation.Animation.from_json("assets/entities/archer/walk_animation.json")
    )
)
eright.add_component(c_sprite.SpriteRendererComponent())
eright.add_component(
    interact.InteractionFieldComponent(collision_mask=0b00000001)
)._velocity.xy = (-40, 5)


edown = ctx.CTX_WORLD.add_entity(entity.Entity())
edown.add_component(c_AABB.AABBColliderComponent(20, 20))
edown.add_component(c_sprite.SpriteComponent())
edown.add_component(
    animation.AnimatedSpriteComponent(
        animation.Animation.from_json("assets/entities/archer/walk_animation.json")
    )
)
edown.add_component(c_sprite.SpriteRendererComponent())
edown.add_component(
    interact.InteractionFieldComponent(collision_mask=0b00000001)
)._velocity.y = -50


some_random_block = ctx.CTX_WORLD.add_entity(entity.Entity())
some_random_block.add_component(c_AABB.AABBColliderComponent(40, 40))
some_random_block.add_component(
    interact.InteractionFieldComponent(collision_mask=0b00000001, static=True)
)
some_random_block.add_component(c_sprite.SpriteComponent())
some_random_block.add_component(
    animation.AnimatedSpriteComponent(
        animation.Animation.from_json("assets/entities/archer/walk_animation.json")
    )
)
some_random_block.add_component(c_sprite.SpriteRendererComponent())

some_random_block._position += pygame.Vector2(300, 200)
eleft._position += pygame.Vector2(200, 200)
eright._position += pygame.Vector2(450, 200)
edown._position += pygame.Vector2(250, 280)


# some_random_block.alive = False
# eleft.alive = False
# edown.alive = False
# eright.alive = False


def kill_static():
    if ctx.CTX_INPUT_HANDLER.get_keyboard_pressed(pygame.K_SPACE):
        print(f"{ctx.RUN_TIME:.5f} | KILLING STATIC")
        some_random_block.alive = False
        print(f"{ctx.RUN_TIME:.5f} | FINISHED SENDING SIGNAL")


t2 = e1.add_component(c_task.TaskComponent("kill_static", kill_static))

# ======================================================================== #
# run game
# ======================================================================== #


ctx.run()
