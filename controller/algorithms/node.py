from typing import Any, Optional
from copy import copy, deepcopy


class Node:
    total_instances = 0
    total_active_instances = 0

    def __init__(
        self,
        value: Any = None,
        next: Optional["Node"] = None,
        prev: Optional["Node"] = None,
    ):
        self.value = value
        self.next = next
        self.prev = prev
        Node.total_instances += 1
        Node.total_active_instances += 1

    def __copy__(self, deep_copy: bool = True) -> "Node":
        if deep_copy:
            return deepcopy(self)
        return copy(self)

    def __eq__(self, other: "Node"):
        return self.value == other.value

    def __repr__(self) -> str:
        return f"Node({self.value!r}, {self.next!r}, {self.prev!r})"
