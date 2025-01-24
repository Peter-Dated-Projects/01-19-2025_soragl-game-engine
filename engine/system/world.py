import pygame

import engine.context as ctx

from engine.ecs import c_task

from engine.graphics import camera

from engine.physics import entity

# ======================================================================== #
# World
# ======================================================================== #


class World2D(entity.Entity):
    def __init__(self, name: str):
        super().__init__()
        self._name = name

        # management information
        self._layers = {}
        self._delta_layers = []

        # rendering information
        self._render_chunk_cache = set()
        self._camera = camera.Camera2D(
            render_distance=4, viewbox=ctx.W_FRAMEBUFFER.get_rect()
        )

        # entity management - entities are just "container" objects
        self._entities = {}
        self._delta_entities = []

        # gamestate parent
        self._gamestate = None

    def __post_init__(self):
        # default task for the aspect handler
        self._entity_chunk_change_task = c_task.Task(
            f"_{ctx.ENGINE_NAME}_entity_chunk_change_task",
            self._entity_chunk_change_task,
        )
        ctx.CTX_ECS_HANDLER.add_component(self._entity_chunk_change_task, self)

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def update(self):

        # TODO - check if camera moved chunks
        self._render_chunk_cache = set(self._camera.generate_visible_chunks())

        # update all layers
        for layer in self._layers.values():
            layer.update()

        # ------------------------------------------------ #
        # finish up by updating layers
        for layer in self._delta_layers:
            self.add_layer(layer)
        self._delta_layers.clear()

        # finish up by updating entities
        for entity in self._delta_entities:
            self.add_entity(entity)
        self._delta_entities.clear()

    def _entity_chunk_change_task(self):
        for entity in self._entities.values():
            # calculate new chunk
            entity._chunk_pos = (
                entity._position.x // ctx.DEFAULT_CHUNK_PIXEL_WIDTH,
                entity._position.y // ctx.DEFAULT_CHUNK_PIXEL_HEIGHT,
            )

            # check if entity moved chunks
            if entity._chunk_pos != entity._prev_chunk_pos:
                # remove entity from old chunk
                self.get_chunk(entity._prev_chunk_pos).remove_entity(entity)
                # add entity to new chunk
                self.get_chunk(entity._chunk_pos).add_entity(entity)
                # update previous chunk position
                entity._prev_chunk_pos = entity._chunk_pos

    # ------------------------------------------------------------------------ #
    # layer logic
    # ------------------------------------------------------------------------ #

    def add_layer(self, layer: "Layer"):
        self._layers[layer._zlevel] = layer

    def remove_layer(self, layer: "Layer"):
        self._delta_layers.append(layer)

    def get_layer(self, zlevel: int):
        return self._layers.get(zlevel)

    # ------------------------------------------------------------------------ #
    # chunk logic
    # ------------------------------------------------------------------------ #

    def add_chunk(self, chunk: "Chunk", zlayer: int):
        if not zlayer in self._layers:
            self._layers[zlayer] = Layer(zlayer)

        self._layers[zlayer].add_chunk(chunk)

    def remove_chunk(self, chunk: "Chunk", zlayer: int):
        if not zlayer in self._layers:
            return

        self._layers[zlayer].remove_chunk(chunk)

    def get_chunk(self, chunk_position: tuple, zlayer: int):
        if not zlayer in self._layers:
            return None

        return self._layers[zlayer].get_chunk(chunk_position)

    # ------------------------------------------------------------------------ #
    # entity logic
    # ------------------------------------------------------------------------ #

    def add_entity(self, entity: "Entity"):
        self._entities[id(entity)] = entity
        entity._world = self
        entity.__post_init__()
        return entity

    def remove_entity(self, entity: "Entity"):
        self._delta_entities.append(entity)

    def get_entity(self, entity_id: int):
        return self._entities.get(entity_id)


# ======================================================================== #
# Layer
# ======================================================================== #


class Layer:
    def __init__(
        self,
        zlevel: int = 0,
        buffer: bool = False,
        buffer_size: tuple = None,
    ):
        self._zlevel = zlevel
        self._chunks = {}
        self._delta_chunks = []
        self._buffer = buffer

        # buffer information -- toggleable
        self._framebuffer = (
            None if not buffer else pygame.Surface(ctx.W_FRAMEBUFFER.get_size())
        )
        self._buffer_size = buffer_size

        # management information
        self._world = None

    def __post_init__(self):
        pass

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def update(self):
        # update all chunks inside of this layer
        # TODO - add valid chunk filtering
        #       - something like: self._world.get_visible_chunks(self)
        for chunk in self._chunks.values():
            chunk.update()

        # finish up by updating chunks
        for chunk in self._delta_chunks:
            self.add_chunk(chunk)
        self._delta_chunks.clear()

    # ------------------------------------------------------------------------ #
    # chunk logic
    # ------------------------------------------------------------------------ #

    def add_chunk(self, chunk: "Chunk"):
        self._chunks[id(chunk)] = chunk
        chunk._layer = self
        chunk.__post_init__()

    def remove_chunk(self, chunk: "Chunk"):
        self._delta_chunks.append(chunk)

    def get_chunk(self, chunk_position: tuple):
        return self._chunks.get(Chunk.get_id(chunk_position))


# ======================================================================== #
# Chunk
# ======================================================================== #


class Chunk:

    @staticmethod
    def get_id(chunk_position: tuple):
        return f"{int(chunk_position[0])}||{int(chunk_position[1])}"

    # ------------------------------------------------------------------------ #
    # init
    # ------------------------------------------------------------------------ #

    def __init__(self, chunk_position: tuple):
        self._chunk_position = chunk_position
        self._chunk_size = (
            ctx.DEFAULT_CHUNK_PIXEL_WIDTH,
            ctx.DEFAULT_CHUNK_PIXEL_HEIGHT,
        )

        # chunk information
        self._chunk_id = Chunk.get_id(self._chunk_position)

        # management information
        self._layer = None

        # entity information
        # TODO - add entities
        self._entities = {}
        self._delta_entities = []

    def __post_init__(self):
        pass

    # ------------------------------------------------------------------------ #
    # logic
    # ------------------------------------------------------------------------ #

    def update(self):
        # update all entities inside of this chunk

        # finish up by updating entities
        for entity in self._delta_entities:
            self.add_entity(entity)
        self._delta_entities.clear()

    # ------------------------------------------------------------------------ #
    # entity logic
    # ------------------------------------------------------------------------ #

    def add_entity(self, entity: "Entity"):
        self._entities[id(entity)] = entity

    def remove_entity(self, entity: "Entity"):
        self._delta_entities.append(entity)

    # ------------------------------------------------------------------------ #
    # special logic
    # ------------------------------------------------------------------------ #

    def __id__(self):
        return self._chunk_id
