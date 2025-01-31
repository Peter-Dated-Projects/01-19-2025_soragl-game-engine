import pygame

import engine.context as ctx

from engine.physics import interact
from engine.physics.ecs import c_AABB

import engine.ecs.c_sprite as c_sprite

# ------------------------------------------------------------------------ #
# resolve aabb aabb
# ------------------------------------------------------------------------ #


def _resolve_aabb_aabb(manifold: interact.CollisionManifold):
    interact1 = manifold._interact1
    interact2 = manifold._interact2
    entity1 = interact1._entity
    entity2 = interact2._entity
    rect1 = pygame.FRect(entity1._prev_position.copy(), interact1._shape._rect.size)
    rect2 = pygame.FRect(entity2._prev_position.copy(), interact2._shape._rect.size)

    # calculate expected movement velocities
    # applying this value will not result in 100% accuracy
    # but it will be close enough
    ndis = (
        entity2._position - entity1._position + pygame.Vector2(0.0001, 0.0001)
    ).normalize()
    v1f = (
        interact1._velocity
        - ((2 * interact2._mass) / (interact1._mass + interact2._mass))
        * ((interact1._velocity - interact2._velocity).dot(ndis))
        * ndis
    )
    v2f = (
        interact2._velocity
        - ((2 * interact1._mass) / (interact1._mass + interact2._mass))
        * ((interact2._velocity - interact1._velocity).dot(ndis))
        * ndis
    )

    # x axis
    rect1.centerx = entity1._position.x
    rect2.centerx = entity2._position.x

    # print("BEFORE HIT")
    # print(rect1, rect2)
    # print(entity1._position, entity2._position)
    # print(v1f, v2f)
    # print(interact1._mass, interact2._mass)

    # print("CHECKING X AXIS")

    if rect1.colliderect(rect2):
        interact1._velocity.x = v1f.x
        interact2._velocity.x = v2f.x

        # print(f"{ctx.RUN_TIME:.5f} | PENETRATION: {manifold._extra['penetration']}")

        if interact1._static:
            interact1._velocity.x = 0
            rect2.x += manifold._extra["penetration"].x
        elif interact2._static:
            interact2._velocity.x = 0
            rect1.x += manifold._extra["penetration"].x
        else:
            rect1.x -= manifold._extra["penetration"].x
            rect2.x += manifold._extra["penetration"].x
    # print(f"{ctx.RUN_TIME:.5f} | RECTS:", rect1, rect2)
    # print(f"{ctx.RUN_TIME:.5f} | COLLIDING:", rect1.colliderect(rect2))

    # y axis
    rect1.centery = entity1._position.y
    rect2.centery = entity2._position.y

    # print(rect1.left, rect1.right, rect2.left, rect2.right)
    # print("CHECKING Y AXIS")

    if rect1.colliderect(rect2):
        interact1._velocity.y = v1f.y
        interact2._velocity.y = v2f.y

        # print(f"{ctx.RUN_TIME:.5f} | PENETRATION: {manifold._extra['penetration']}")

        if interact1._static:
            interact1._velocity.y = 0
        elif interact2._static:
            interact2._velocity.y = 0
        else:
            rect1.y -= manifold._extra["penetration"].y
            rect2.y += manifold._extra["penetration"].y

    # update positions
    entity1._position.xy = rect1.center
    entity2._position.xy = rect2.center

    # print("AFTER HIT")
    # print(entity1._position, entity2._position)
    # print(interact1._static, interact2._static)
    # print(interact1._velocity, interact2._velocity)
    # print(rect1.colliderect(rect2))

    # ctx.stop()


interact.InteractionField.cache_resolution_function(
    c_AABB.AABBColliderComponent, c_AABB.AABBColliderComponent, _resolve_aabb_aabb
)
