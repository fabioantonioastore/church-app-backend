from controller.algorithms.node import Node
from copy import deepcopy
from typing import Any, NoReturn

class Stack():
    total_stacks: int = 0
    total_instances: int = 0
    def __init__(self) -> NoReturn:
        self.first = None
        self.last = None
        self.size = 0
        Stack.total_stacks += 1
        Stack.total_instances += 1

    @classmethod
    def get_total_stacks(cls) -> int:
        return cls.total_stacks

    @classmethod
    def get_total_instances(cls) -> int:
        return cls.total_instances

    def __del__(self) -> NoReturn:
        Stack.total_stacks -= 1

    def add(self, value: Any = None) -> NoReturn:
        value = deepcopy(value)
        node = Node(value)
        self.size += 1
        if self.first is None:
            self.first = node
            self.last = self.first
            return
        if self.first is self.last:
            self.first = node
            self.first.put_next(self.last)
            self.last.put_prev(self.first)
            return
        node.put_next(self.first)
        self.first.put_prev(node)
        self.first = node

    def to_list(self) -> list:
        node = self.first
        node_list = []
        while not(node is None):
            node_list.append(node.get_value())
            node = node.get_next()
        return deepcopy(node_list)

    def to_generator(self) -> tuple:
        node = self.first
        while not(node is None):
            yield deepcopy(node.get_value())
            node = node.get_next()

    def pop(self) -> Any:
        if self.first is None: return
        self.size -= 1
        if self.first is self.last:
            value = self.first.get_value()
            self.first = None
            self.last = None
            return deepcopy(value)
        value = self.first.get_value()
        node = self.first
        self.first = self.first.get_next()
        self.first.put_prev(None)
        del node
        return deepcopy(value)

    def get_size(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "Stack()"