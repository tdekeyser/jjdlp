'''
Builds writing pathways as Tree object
'''
from connect.core import Node, BranchedTree, Branch
from connect.db import DatabaseQuery


class PathwayNode(Node):
    '''
    @param: DatabaseObject pathObject:
        An object from database, e.g. a Notebook instance.
    @param: Node parent:
        A parent Node object.
    '''
    __slots__ = ('dbObject', 'referent')

    def __init__(self, dbObject, parent):
        self.dbObject = dbObject
        self.referent = str(dbObject.__class__.__name__).lower()
        # get name and call super constructor
        super(PathwayNode, self).__init__(str(self.dbObject), parent)

    def jsonify(self):
        # override
        export = super(PathwayNode, self).jsonify()
        export['referent'] = self.referent
        export['pk'] = self.dbObject.pk
        return export


class PathwayBranch(Branch):
    '''
    One single path within a PathwayTree object.
    Overrides some methods to add constraints in order
    to avoid enormous branches.
    '''
    def select(self, nodeName, **kwargs):
        '''
        Make it impossible to select the root as branch, as
        this would return the complete tree.
        '''
        # override
        layer, node = self.tree.get_node(nodeName)
        if layer != 0:
            super(PathwayBranch, self).select(nodeName, **kwargs)

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
                    c = self.find_descendants(child)
                    if len(c) < 10:
                        desc = desc | c
        return desc

class PathwayTree(BranchedTree):
    '''
    @param: String root
    @param: String rootModel
    '''
    dbquery = None

    def __init__(self, root, rootModel):
        super(PathwayTree, self).__init__(root)
        # load models
        self.dbquery = DatabaseQuery()
        # reset root node
        self.reset_root(self.root, model=rootModel)

    def init_branch(self, root):
        # override
        self.branch = PathwayBranch(self)

    def reset_root(self, rootNode, model=''):
        rootObj = self.dbquery.get(rootNode, model=model)
        baseNode = PathwayNode(rootObj, None)
        self.root = baseNode
        # remove Node root
        self.graph.pop()
        # add PathwayNode root
        self.graph.add((0, baseNode))

    def get_model_children(self, parentNode):
        # get child query
        ds = self.dbquery.query(parentNode, downstream=True)
        us = self.dbquery.query(parentNode, upstream=True)
        return ds+us

    def get_children(self, parentNode):
        # override
        child_objects = self.get_model_children(parentNode)
        return set([PathwayNode(child, parentNode) for child in child_objects])
