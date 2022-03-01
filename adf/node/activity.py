from adf.node.node import Node


class Activity(Node):
    rootType = "Microsoft.DataFactory/factories/pipelines"

    @classmethod
    def default_kls(cls):
        return DefaultActivity

    def __init__(
        self,
        file,
        type,
        name,
        description=None,
        policy=None,
        dependsOn=(),
        typeProperties={},
        userProperties=(),
    ):
        super().__init__(file, type, name)
        self.desc = description
        self.policy = policy
        self.depsOK = [
            d["activity"] for d in dependsOn if "Succeeded" in d["dependencyConditions"]
        ]
        self.depsKO = [
            d["activity"] for d in dependsOn if "Failed" in d["dependencyConditions"]
        ]
        self.depsAny = [
            d["activity"] for d in dependsOn if "Completed" in d["dependencyConditions"]
        ]
        assert not (
            set(d["activity"] for d in dependsOn)
            - set(self.depsOK + self.depsKO + self.depsAny)
        )
        self.init(**typeProperties)
        self.userProps = userProperties

    def init(self, **kwargs):
        self.props = kwargs

    def sibling(self, name):
        (node,) = Activity.filter(
            lambda n: n.file == self.file and n.type != self.rootType and n.name == name
        )
        return node

    def resolve(self):
        self.depsOK = [self.sibling(name) for name in self.depsOK]
        self.depsKO = [self.sibling(name) for name in self.depsKO]
        self.depsAny = [self.sibling(name) for name in self.depsAny]

    def key(self):
        if self.type == self.rootType:
            return f"{self.file}-root"
        else:
            return f"{self.file}-{self.name}"

    def link_deps(self, g):
        for dep in self.depsOK:
            g.edge(dep.key_out(), self.key_in(), color="green")
        for dep in self.depsKO:
            g.edge(dep.key_out(), self.key_in(), color="red")
        for dep in self.depsAny:
            g.edge(dep.key_out(), self.key_in(), color="grey")

    def draw(self, g, **kwargs):
        super().draw(g, **kwargs)
        self.link_deps(g)

    def link_graph(self, g, nodes, **kwargs):
        names = set(n.name for n in nodes)
        head = set()
        tail = set(n.name for n in nodes)
        for node in nodes:
            deps = (
                set(d.name for d in (node.depsOK + node.depsKO + node.depsAny)) & names
            )
            if not deps:
                head.add(node.name)
            else:
                tail = tail - deps
        head, tail = [self.sibling(h) for h in head], [self.sibling(t) for t in tail]
        for h in head:
            g.edge(self.key_in(), h.key_in(), **kwargs)
        for t in tail:
            g.edge(t.key_out(), self.key_out(), **kwargs)

    def export(self):
        return {
            **super().export(),
            "desc": self.desc,
            "policy": self.policy,
            "props": self.props,
        }


class DefaultActivity(Activity):
    pass
