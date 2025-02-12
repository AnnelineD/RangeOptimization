

class Node:
    def __init__(self, cd, l):
        self.idc = len(l) # node id
        self.cd = cd      # dict of outgoing edges
        l.append(self)

    def paths(self):
        for k, v in self.cd.items():
            if isinstance(v, Node):
                for p in v.paths():
                    yield [k] + p
            else:
                yield [k]

    def graphviz(self):
        for k, v in self.cd.items():
            if isinstance(v, Node):
                print(f"n{self.idc} -> n{v.idc} [label={k}]")
            else:
                print(f"n{self.idc} -> {k}")

    def full_dict(self):
        def rec(n):
            return {k: rec(v) for k, v in n.cd.items()} if isinstance(n, Node) else str(n)

        return {k: rec(v) for k, v in self.cd.items()}

    def __repr__(self):
        nested = {k: str(v) for k, v in self.cd.items()}
        return f"N({self.idc}, {nested})"

    def __str__(self):
        return f"N{self.idc}"