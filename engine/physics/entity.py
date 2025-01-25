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
        self._layer = None
        self._world = None

        # component handler
        self._components: dict[str, Component] = {}

        # basic information
        self._prev_position = pygame.Vector2()
        self._prev_chunk_pos = (0, 0)
        self._prev_zlayer = 0
        self._position = pygame.Vector2()
        self._chunk_pos = (0, 0)
        self._zlayer = 0

        self._rect = pygame.Rect()

    def __post_init__(self):
        # override in subclasses
        pass

    # ------------------------------------------------------------------------ #
    # component logic
    # ------------------------------------------------------------------------ #

    def add_component(self, component):
        # add to ecs -- if component not in ecs
        self._world._gamestate._ecs.add_component(component, self)

        return component

    def remove_component(self, component):
        self._components.pop(id(component))

    def get_components(self, component_class: type):
        return [
            component
            for component in self._components.values()
            if isinstance(component, component_class)
        ]

    def get_component_by_id(self, component_id: int):
        return (
            self._components[component_id] if component_id in self._components else None
        )

    def iterate_components(self, component_class: type):
        for component in self._components.values():
            if isinstance(component, component_class):
                yield component

    def handle_components(self):
        for component in self._components.values():
            component.update()

    # ------------------------------------------------------------------------ #
    # special properties
    # ------------------------------------------------------------------------ #

    def __hash__(self):
        return self._entity_id

    @property
    def zlayer(self):
        return self._zlayer

    @zlayer.setter
    def zlayer(self, value):
        self._prev_zlayer = self._zlayer
        self._zlayer = value
