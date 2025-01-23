import pygame

# ======================================================================== #
# Entity
# ======================================================================== #


class Entity:
    ENTITY_ID_COUNTER = 0

    @staticmethod
    def generate_entity_id():
        Entity.ENTITY_ID_COUNTER += 1
        return Entity.ENTITY_ID_COUNTER

    # ------------------------------------------------------------------------ #
    # init
    # ------------------------------------------------------------------------ #

    def __init__(self):
        self._entity_id = Entity.generate_entity_id()

        # component handler
        self._components: dict[str, Component] = {}

        # basic information
        self._prev_position = pygame.Vector3()
        self._prev_chunk_pos = (0, 0)

        self._position = pygame.Vector3()
        self._chunk_pos = (0, 0)

        self._rect = pygame.Rect()

    # ------------------------------------------------------------------------ #
    # component logic
    # ------------------------------------------------------------------------ #

    def add_component(self, component):
        self._components[id(component)] = component

    def remove_component(self, component):
        self._components.pop(id(component))

    def get_components(self, component_class: type):
        return [
            component
            for component in self._components.values()
            if isinstance(component, component_class)
        ]

    def iterate_components(self, component_class: type):
        for component in self._components.values():
            if isinstance(component, component_class):
                yield component
