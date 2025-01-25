from abc import ABC, abstractmethod


# ======================================================================== #
# aspect component handler
# ======================================================================== #


class ECSHandler:
    COMPONENT_UUID_COUNTER = 0

    def __init__(self):
        # ecs management
        self._components = {}

        # gamestate parent
        self._gamestate = None

    def __post_init__(self):
        pass

    @classmethod
    def generate_aspect_uuid(cls):
        cls.ASPECT_UUID_COUNTER += 1
        return cls.ASPECT_UUID_COUNTER

    @classmethod
    def generate_component_uuid(cls):
        cls.COMPONENT_UUID_COUNTER += 1
        return cls.COMPONENT_UUID_COUNTER

    # -------------------------------------------------------------------- #
    # component logic
    # -------------------------------------------------------------------- #

    def add_component(self, component, entity):
        # check if component added to entity
        entity._components[component._uuid] = component
        component._ecs_handler = self
        component._entity = entity
        component.__post_init__()

        # create section for component if not exists
        if not component.__class__ in self._components:
            self._components[component.__class__] = {}

        # add component to the cache
        self._components[component.__class__][component._uuid] = component

    def remove_component(self, component):
        # remove component from the components
        if not component.__class__ in self._components:
            return

        # remove from entity as well
        component._entity.remove_component(component)

        # remove component from the cache
        del self._components[component.__class__][component._uuid]

    def iterate_components(self, component_class: type):
        for component in self._components[component_class].values():
            yield component

    def get_component(self, component_class: type, uuid):
        return self._components[component_class][uuid]

    def get_components(self, component_class: type):
        return self._components[component_class].values()


# ======================================================================== #
# component
# ======================================================================== #


class Component:
    def __init__(self, name: str):
        self.name = name

        self._uuid = 0
        self._ecs_handler = None

        self._entity = None

    def __post_init__(self):
        if not self._uuid:
            self._uuid = ECSHandler.generate_component_uuid()

    # -------------------------------------------------------------------- #
    # logic
    # -------------------------------------------------------------------- #

    @abstractmethod
    def update(self):
        pass
