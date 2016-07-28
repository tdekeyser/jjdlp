'''
Conversion for Tree graph into usable graph formats of
nodes and edges.
'''


class Layout(object):

    def __init__(self, obj):
        self.obj = obj
        self.layout = {}
        self.build_layout(obj)

    def build_layout(self, obj):
        pass


class GraphLayout(Layout):
    '''
    Converts the default Tuple layout of Tree objects into
    an undirected graph of nodes and edges.
    {
    "nodes": [{
        "name": String,
        "layer": int
        },
        ...],
    "edges": [{
        "source": index_of_node,
        "target": index_of_node
        }]
    }
    '''
    def build_layout(self, obj):
        # override
        self.build_nodes(obj)
        self.build_edges(obj)

    def build_nodes(self, obj):
        nodes = []
        for layer, node in obj.graph:
            json = node.jsonify()
            json['layer'] = layer
            nodes.append(json)
        self.layout['nodes'] = nodes

    def build_edges(self, obj):
        '''
        Create edges dictionary entry of the graph.
        '''
        edges = []
        for i in range(obj.length-1):
            layerNodes = obj.get_layer(i+1)
            for node in layerNodes:
                childIndex = self.get_index(i+1, node)
                for parent in node.parent:
                    try:
                        parentIndex = self.get_index(i, parent)
                        e = {'source': parentIndex, 'target': childIndex}
                        edges.append(e)
                    except ValueError:
                        # node's parent is not part of the branch
                        continue
        self.layout['edges'] = edges

    def get_index(self, layer, node):
        '''
        Get the index of a node within layout['nodes'].
        '''
        json = node.jsonify()
        json['layer'] = layer
        return self.layout['nodes'].index(json)

    def branchlayout(self):
        '''
        Perform graph layout on one branch.
        '''
        self.build_layout(self.obj.branch)
        return self.layout
