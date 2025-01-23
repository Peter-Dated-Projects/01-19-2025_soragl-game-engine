from abc import ABC, abstractmethod


# ======================================================================== #
# aspect component handler
# ======================================================================== #


class ECSHandler:
    COMPONENT_UUID_COUNTER = 0
    ASPECT_UUID_COUNTER = 0

    def __init__(self):
        # ecs management
        self._aspects = {}
        self._components = {}
        self._aspect_order = []

    @classmethod
    def generate_aspect_uuid(cls):
        cls.ASPECT_UUID_COUNTER += 1
        return cls.ASPECT_UUID_COUNTER

    @classmethod
    def generate_component_uuid(cls):
        cls.COMPONENT_UUID_COUNTER += 1
        return cls.COMPONENT_UUID_COUNTER

    # -------------------------------------------------------------------- #
    # aspect logic
    # -------------------------------------------------------------------- #

    def add_aspect(self, aspect):
        aspect.__post_init__()
        aspect._ecs_handler = self

        # register aspect
        self._aspects[aspect._uuid] = aspect

        # add to priority
        self._aspect_order.append(aspect._uuid)
        self._aspect_order.sort(key=lambda x: -self._aspects[x].priority)

        # create sections for all target components
        for component_class in aspect.target_components_classes:
            if not component_class in self._components:
                self._components[component_class] = {}

    def remove_aspect(self, aspect):
        # remove aspect from the list
        del self._aspects[aspect._uuid]

        # remove from the aspect order
        self._aspect_order.remove(aspect._uuid)

    # -------------------------------------------------------------------- #
    # component logic
    # -------------------------------------------------------------------- #

    def add_component(self, component):
        # check if component already loaded
        if component._uuid in self._components:
            return

        # init
        component.__post_init__()
        component._ecs_handler = self

        # find the aspect that has the component
        if not component.__class__ in self._components:
            self._components[component.__class__] = {}

        # add component to the cache
        self._components[component.__class__][component._uuid] = component

    def remove_component(self, component):
        # remove component from the components
        if not component.__class__ in self._aspect_component_map:
            return

        # remove component from the cache
        del self._aspect_component_map[component.__class__][component._uuid]

    def iterate_components(self, component_class: type):
        for component in self._components[component_class].values():
            yield component

    def get_component(self, component_class: type, uuid):
        return self._aspect_component_map[component_class][uuid]

    def get_components(self, component_class: type):
        return self._aspect_component_map[component_class].values()

    # -------------------------------------------------------------------- #
    # logic
    # -------------------------------------------------------------------- #

    def update(self):
        for aspect in self._aspects.values():
            # we use this to order the aspects
            # some have higher priority than others
            aspect.handle_components()


# ======================================================================== #
# aspect
# ======================================================================== #


class Aspect:
    def __init__(
        self, name: str, target_components_classes: list[type], priority: int = 0
    ):
        self.name = name
        self.priority = priority

        self._uuid = 0
        self.target_components_classes = target_components_classes
        self._ecs_handler = None

    def __post_init__(self):
        self._uuid = ECSHandler.generate_aspect_uuid()

    # -------------------------------------------------------------------- #
    # logic
    # -------------------------------------------------------------------- #

    def handle_components(self):
        """This function contains all logic -- and iterates through all components"""
        for component_class in self.target_components_classes:
            for component in self._ecs_handler.iterate_components(component_class):
                component.update()


# ======================================================================== #
# component
# ======================================================================== #


class Component:
    def __init__(self, name: str):
        self.name = name

        self._uuid = 0
        self._ecs_handler = None

    def __post_init__(self):
        self._uuid = ECSHandler.generate_component_uuid()

    # -------------------------------------------------------------------- #
    # logic
    # -------------------------------------------------------------------- #

    @abstractmethod
    def update(self):
        pass
