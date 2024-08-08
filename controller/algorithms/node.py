class Node:
    total_nodes: int = 0
    total_instances: int = 0
    def __init__(self, value = None, next = None, prev = None):
        self.value = value
        self.next = next
        self.prev = prev
        Node.total_nodes += 1
        Node.total_instances += 1

    @classmethod
    def get_total_nodes(cls) -> int:
        return cls.total_nodes

    @classmethod
    def get_total_instances(cls) -> int:
        return cls.total_instances

    def __del__(self):
        Node.total_nodes -= 1

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev

    def put_value(self, new_value):
        self.value = new_value

    def put_next(self, new_next):
        self.next = new_next

    def put_prev(self, new_prev):
        self.prev = new_prev

    def __repr__(self):
        return f"Node({self.value!r}, {self.get_next()!r}, {self.get_prev()!r})"