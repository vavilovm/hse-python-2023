import ast
import inspect
import os
import networkx


def node_name(v):
    return v.__class__.__name__


class GraphBuilder:
    def __init__(self):
        self.graph = networkx.DiGraph()
        self.graph.node_attr_dict_factory = lambda: {'style': 'filled', 'shape': 'box3d'}

    def build(self, v):
        return getattr(self, '_' + node_name(v))(v)

    def add_edges(self, root, nodes, edges_name=''):
        for v in nodes:
            self.graph.add_edge(root, v, label=edges_name)

    def add_node(self, v, fillcolor=None, label=None, shape=None):
        if label is None:
            label = node_name(v)
        if fillcolor is None:
            fillcolor = 'white'
        if shape is None:
            shape = 'box3d'
        self.graph.add_node(v, label=label, fillcolor=fillcolor, shape=shape)

    def _Module(self, v):
        self.add_node(v, label='Module', fillcolor='lightgrey')
        self.add_edges(v, self.build(v.body[0]))
        return [v]

    def _arguments(self, v):
        self.add_node(v, fillcolor='#6B8E23')
        for arg in v.args:
            self.add_node(arg, label=f'arg {arg.arg}', fillcolor='#48D1CC')
            self.add_edges(v, [arg])
        return [v]

    def _Constant(self, v):
        self.add_node(v, shape='house', label=f'Constant {v.value}',
                      fillcolor='#2E8B57')
        return [v]

    def _FunctionDef(self, v):
        self.add_node(v, label=f'Function {v.name}', fillcolor='#00FF00')
        self.add_edges(v, self.build(v.args))
        for body in v.body:
            self.add_edges(v, self.build(body))
        return [v]

    def _BinOp(self, v):
        op = node_name(v.op)
        self.add_node(v, label=f'BinOp {op}', fillcolor='#778899')
        self.add_edges(v, self.build(v.left), 'left')
        self.add_edges(v, self.build(v.right), 'right')
        return [v]

    def _Compare(self, v):
        label = 'Compare'
        if len(v.ops) == 1:
            label = 'Compare ' + node_name(v.ops[0])
        self.add_node(v, label=label, fillcolor='orange')

        self.add_edges(v, self.build(v.left), 'left')

        if len(v.ops) > 1:
            for op in v.ops:
                opname = op.__class__.__name__
                self.add_node(op, label=f'{opname}', fillcolor='blue')
                self.graph.add_edge(v, op, label='op')

        for comp in v.comparators:
            self.add_edges(v, self.build(comp), 'comp')
        return [v]

    def _For(self, v):
        self.add_node(v, shape='triangle', fillcolor='coral')
        self.add_edges(v, self.build(v.target))
        self.add_edges(v, self.build(v.iter))
        for body in v.body:
            self.add_edges(v, self.build(body))
        return [v]

    def _If(self, v):
        self.add_node(v,
                      shape='diamond',
                      fillcolor='lightblue')
        self.add_edges(v, self.build(v.test), 'test')
        for or_else in v.orelse:
            self.add_edges(v, self.build(or_else), 'or else')
        for body in v.body:
            self.add_edges(v, self.build(body), 'body')
        return [v]

    def _Assign(self, v):
        self.add_node(v, fillcolor='yellow')
        for target in v.targets:
            self.add_edges(v, self.build(target), 'target')
        self.add_edges(v, self.build(v.value), 'value')
        return [v]

    def _Return(self, v):
        self.add_node(v, shape='octagon', fillcolor='#9370DB')
        self.add_edges(v, self.build(v.value))
        return [v]

    def _Raise(self, v):
        self.add_node(v, shape='octagon', fillcolor='#9370DB')
        self.add_edges(v, self.build(v.exc))
        return [v]

    def _List(self, v):
        self.add_node(v, fillcolor='pink')
        for elt in v.elts:
            self.add_edges(v, self.build(elt))
        return [v]

    def _Subscript(self, v):
        self.add_node(v, fillcolor='green')
        self.add_edges(v, self.build(v.value), 'value')
        self.add_edges(v, self.build(v.slice), 'slice')
        return [v]

    def _Call(self, v):
        self.add_node(v, fillcolor='#6495ED')
        self.add_edges(v, self.build(v.func), 'func')
        for arg in v.args:
            self.add_edges(v, self.build(arg), 'arg')
        return [v]

    def _Name(self, v):
        self.add_node(v, shape='egg', label=f'Name {v.id}', fillcolor='#BDB76B')
        return [v]


def create_ast_graph(ast_object):
    v = GraphBuilder()
    v.build(ast_object)
    pdot = networkx.drawing.nx_pydot.to_pydot(v.graph)
    pdot.set_bgcolor("beige")
    return pdot


# return fibonacci sequence of length n
def fibonacci(n):
    fib = [1] * n
    if n < 0:
        raise ValueError("n must be a positive integer")
    if n == 0:
        return []
    elif n <= 2:
        return fib
    for i in range(2, n):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib


def create_ast_image(f):
    f_ast = ast.parse(inspect.getsource(f))
    g = create_ast_graph(f_ast)
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    g.write_png('artifacts/graph.png')

def create_fib_ast_image():
    create_ast_image(fibonacci)


if __name__ == '__main__':
    create_fib_ast_image()
