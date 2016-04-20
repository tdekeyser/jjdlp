'''
Basic tree graph building classes
=================================
The `Tree` class iteratively builds simple tree structures,
represented as a set of nodes accompanied with layer numbers.

The `Branch` class selects a single branch from a `Tree` object
based on a Node name. It is possible to remove either ancestors
or descendants from the branch. Setting

    Branch.select(String unit, anc=True, desc=True)

arguments to `False` removes either ancestors or
descendans from the branch.

`BranchedTree` combines the two previous in one class for
simplicity.

    >> t = Tree('root')
    >> print t
    [(0, None/root)]
    >> t.grow(2)
    >> print t
    [(0, None/root), (1, root/unit297), (1, root/unit280),
    (2, unit280/unit517), (2, unit280/unit791), (2, unit297/unit850),
    (2, unit297/unit659)]

    >> b = Branch(t)
    >> b.select('unit297')
    >> print b
    [(0, None/root), (1, root/unit297), (2, unit297/unit850),
    (2, unit297/unit659)]

    >> bt = BranchedTree('root')
    >> bt.grow(4)
    >> bt.select_branch('unitX')
    >> print bt.branch

@author: Tom De Keyser
'''
from random import randrange


class Node(object):
    '''
    Most basic component of a tree/branch.

    @param: String name
    @param: Node parent
    '''
    __slots__ = ('name', 'parent')

    def __init__(self, name, parent):
        self.name = name
        self.parent = [parent] if parent else []

    def __str__(self):
        return u'{}'.format(self.name)

    def __repr__(self):
        return '{0}/{1}'.format(
            self.parent,
            self.name
            )

    def __hash__(self):
        # set hash definition
        return hash(self.name)

    def __eq__(self, other):
        # set comparison
        return self.name == other.name

    def jsonify(self):
        # returns indentifiers for layout
        export = {}
        export['name'] = self.name
        return export


class Tree(object):
    # PERHAPS MAKE SOME NAMED_TUPLE HERE?
    '''
    A Tree graph is a set of tuples (int layer, Node node).
    Uses a limited breadth-first method to develop each layer.

    @param: String root
    '''
    root = None
    graph = set()
    length = 0

    def __init__(self, root):
        self.graph = set()
        self.graph_depth = 0
        # graph is a set of tuples (layer, Node)
        self.set_root(root)

    def __repr__(self):
        return str(sorted(self.graph))

    def get_layer(self, layerNr):
        # get all nodes from one layer
        return set(node for layer, node in self.graph if layer == layerNr)

    def count_layer(self, layer):
        return self.graph.count(layer)

    def get_node(self, reqName):
        for layer, node in self.graph:
            if node.name == reqName:
                return (layer, node)
        raise IOError('Cannot find match with "{}".'.format(repr(reqName)))

    def set_root(self, root):
        baseNode = Node(root, None)
        self.root = baseNode
        self.graph.add((0, baseNode))

    def grow(self, max_layer):
        '''Perform limited breadth-first expansion'''
        depth = 0
        while True:
            if (depth == max_layer):
                self.length = depth + 1
                return
            else:
                for node in self.get_layer(depth):
                    self.expand_all_children(depth, node)
                depth += 1

    def expand_all_children(self, depth, parent):
        children = self.get_children(parent)
        for child in children:
            for l, n in self.graph:
                # find common children
                if child == n:
                    if l == depth+1:
                        n.parent.append(parent)
                    else:
                        # avoid loops
                        break
            else:
                self.graph.add((depth + 1, child))
            continue

    def get_children(self, parentNode):
        # test, should be overridden
        toyChld = []
        for i in range(2):
            n = Node('unit'+str(randrange(1000)), parentNode)
            toyChld.append(n)
        return toyChld


class Branch(object):
    '''
    One path within a tree from the bottom to top.
    Subset of a Tree graph for which all Nodes are
    the parent of the following, and for which no
    two tuples contain the same layer number.

    @param: Tree tree; a Tree object
    '''
    tree = None
    graph = set()
    length = 0

    def __init__(self, tree):
        self.tree = tree
        self.graph = set()

    def __repr__(self):
        return str(sorted(self.graph))

    def get_layer(self, layerNr):
        # get node form layer
        return set(node for layer, node in self.graph if layer == layerNr)

    def update(self, updateTree):
        # reallocate the tree
        self.tree = updateTree

    def select(self, nodeName, anc=True, desc=True):
        # first remove previous graph
        self.graph.clear()
        # compile a graph from an input node name
        tup = self.tree.get_node(nodeName)
        self.graph.add(tup)
        # get ancestors and descendants
        ancs = self.find_ancestors(tup) if anc else set()
        descs = self.find_descendants(tup) if desc else set()
        # merge graph
        self.graph = self.graph | ancs | descs
        self.length = len(self.graph)

    def find_ancestors(self, nodeTuple):
        '''
        Perform bottom-to-top depth-first node finding.
        Allows the possibility of multiple parents.
        '''
        layer, node = nodeTuple
        anc = set()
        for i in range(layer-1, self.tree.length-1):
            for n in self.tree.get_layer(i):
                if n in node.parent:
                    parent = (i, n)
                    anc.add(parent)
                    # merge with ancestors of parent
                    anc = anc | self.find_ancestors(parent)
        return anc

    def find_descendants(self, nodeTuple):
        '''
        Perform top-to-bottom depth-first node finding.
        Allows the possibility of multiple children.
        '''
        layer, node = nodeTuple
        desc = set()
        for i in range(layer+1, self.tree.length+1):
            for n in self.tree.get_layer(i):
                if node in n.parent:
                    child = (i, n)
                    desc.add(child)
                    # merge with descendants of child
                    desc = desc | self.find_descendants(child)
        return desc


class BranchedTree(Tree):
    '''
    Combines the Tree and Branch classes in order to be able
    to develop a Tree object that can dynamically change a
    branch of interest from the Tree object.
    '''
    branch = None
    branchBase = ()

    def __init__(self, root):
        super(BranchedTree, self).__init__(root)
        # create root branch
        self.init_branch(root)
        self.branchBase = (root, False, False)
        self.select_branch(root, anc=False, desc=False)

    def select_branch(self, nodeName, anc=True, desc=True):
        self.branch.select(nodeName, anc=anc, desc=desc)
        self.branchBase = (nodeName, anc, desc)

    def grow(self, max_layer):
        # override
        super(BranchedTree, self).grow(max_layer)
        self.branch.update(self)
        self.update_branch()

    def init_branch(self, root):
        self.branch = Branch(self)

    def update_branch(self):
        try:
            nodeName, anc, desc = self.branchBase
            self.select_branch(nodeName, anc=anc, desc=desc)
        except IOError:
            self.select_branch(self.root.name, anc=False, desc=False)
