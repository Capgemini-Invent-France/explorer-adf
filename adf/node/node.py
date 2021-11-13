import json

from graphviz import Digraph

_types = {}
_nodes = {}


class Node:
    defaultType = None
    shape = (None,)

    def __init_subclass__(cls, /, dfType=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if dfType is not None:
            _types[dfType] = cls

    def __new__(cls, type, **kwargs):
        return super().__new__(_types[type])

    def __init__(self, file, type, name):
        self.file = file
        self.type = type
        self.name = name
        assert self.key() not in _nodes
        _nodes[self.key()] = self

    @classmethod
    def filter(cls, f=None):
        return (n for n in filter(f, _nodes.values()) if isinstance(n, cls))

    @classmethod
    def load(cls, path):
        with path.open("r") as f:
            data = json.load(f)
        type = data.pop("type", cls.defaultType)
        typeProperties = data.pop("properties")
        Node(type=type, file=path.stem, typeProperties=typeProperties, **data)

    def resolve(self):
        pass

    @staticmethod
    def resolve_all():
        for node in Node.filter():
            node.resolve()

    def key(self):
        return f"{self.type}-{self.name}"

    def key_in(self):
        if len(self.shape) == 1:
            return self.key()
        else:
            return f"{self.key()}-in"

    def key_out(self):
        if len(self.shape) == 1:
            return self.key()
        else:
            return f"{self.key()}-out"

    def label(self):
        return self.name

    def draw(self, g, **kwargs):
        if len(self.shape) == 1:
            g.node(self.key(), self.label(), shape=self.shape[0], **kwargs)
        else:
            shape_in, shape_out = self.shape
            g.node(self.key_in(), self.label(), shape=shape_in, **kwargs)
            g.node(self.key_out(), self.label(), shape=shape_out, **kwargs)

    @staticmethod
    def draw_all(path, f=None):
        g = Digraph("G", filename=str(path))
        for node in Node.filter(f):
            node.draw(g)
        return g

    def export(self):
        return {
            "file": self.file,
            "type": self.type,
            "name": self.name,
        }

    @staticmethod
    def export_all(f=None):
        return [n.export() for n in Node.filter(f)]
