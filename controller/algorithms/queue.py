from controller.algorithms.node import Node
from copy import deepcopy
from typing import Any, NoReturn

class Queue:
    total_queues: int = 0
    total_instances: int = 0
    def __init__(self) -> NoReturn:
        self.first = None
        self.last = None
        self.size = 0
        Queue.total_queues += 1
        Queue.total_instances += 1

    @classmethod
    def get_total_queues(cls) -> int:
        return cls.total_queues

    @classmethod
    def get_total_instances(cls) -> int:
        return cls.total_instances

    def __del__(self) -> NoReturn:
        Queue.total_queues -= 1

    def add(self, value: Any = None) -> NoReturn:
        value = deepcopy(value)
        node = Node(value)
        self.size += 1
        if self.first is None:
            self.first = node
            self.last = self.first
            return
        if self.first is self.last:
            self.last = node
            self.last.put_prev(self.first)
            self.first.put_next(self.last)
            return
        self.last.put_next(node)
        node.put_prev(self.last)
        self.last = node

    def pop(self) -> Any:
        if self.first is None: return
        value = self.first.get_value()
        self.size -= 1
        if self.first is self.last:
            self.first = None
            self.last = None
            return value
        node = self.first
        self.first = self.first.get_next()
        self.first.put_prev(None)
        del node
        return value

    def to_list(self) -> list:
        node = self.first
        to_list = []
        while not(node is None):
            to_list.append(node.get_value())
            node = node.get_next()
        return deepcopy(to_list)

    def to_generator(self) -> tuple:
        node = self.first
        while not(node is None):
            yield deepcopy(node.get_value())
            node = node.get_next()

    def get_size(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "Queue()"