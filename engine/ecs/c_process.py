from engine.system import ecs

from typing import Callable
from abc import ABC, abstractmethod

import threading
import multiprocessing
import asyncio


"""

Start of with simple process handling
- threading
- coroutines
- multiprocessing

"""

TYPE_THREAD = "thread"
TYPE_COROUTINE = "coroutine"
TYPE_MULTIPROCESSING = "multiprocessing"


# ======================================================================== #
# process
# ======================================================================== #


class Process(ecs.Component):
    def __init__(self, name: str, func: Callable, *args, run_type: str = TYPE_THREAD):
        super().__init__(self.__class__.__name__)
        self.name = name

        self._func = func
        self._args = args

        self._run_type = run_type

    # -------------------------------------------------------------------- #
    # process logic
    # -------------------------------------------------------------------- #

    @abstractmethod
    def run(self):
        pass


# subclasses


class ThreadProcess(Process):
    def __init__(self, name: str, func: Callable, *args):
        super().__init__(name, func, *args, run_type=TYPE_THREAD)

    def run(self):
        pass


class CoroutineProcess(Process):
    def __init__(self, name: str, func: Callable, *args):
        super().__init__(name, func, *args, run_type=TYPE_COROUTINE)

    def run(self):
        pass


class MultiProcessingProcess(Process):
    def __init__(self, name: str, func: Callable, *args):
        super().__init__(name, func, *args, run_type=TYPE_MULTIPROCESSING)

    def run(self):
        pass


# TODO - add threading
# TODO - add coroutines
# TODO - add multiprocessing


# ======================================================================== #
# process handler
# ======================================================================== #


class ProcessAspect(ecs.Aspect):
    def __init__(self):
        super().__init__(self.__class__.__name__, [Process])

    # -------------------------------------------------------------------- #
    # process logic
    # -------------------------------------------------------------------- #

    def handle(self, process):
        # TODO - implement later
        print("Not implemented")
        pass
