# from connect.db import isParent, check_parent_similarity

# def isParent(node):
#     # check whether modelName is a parent model
#     if node.referent in [LIBRARY_ITEM, NOTEBOOKS_NOTEBOOK]:
#         return True
#     else:
#         return False


# def check_parent_similarity(childNode, parentNode):
#     # check if childNode has parentNode as a Foreign Key
#     childObj = childNode.pathObject
#     parentObj = parentNode.pathObject
#     # check library excerpt
#     if childNode.referent == LIBRARY_EXCERPT:
#         if childObj.item.pk == parentObj.pk:
#             return True
#     # check note
#     elif childNode.referent == NOTEBOOKS_NOTE:
#         if childObj.noteb.pk == parentObj.pk:
#             return True
#     return False



# class ComponentOrderMixin(object):
#     '''
#     Provides componentwise ordering of a tuple graph
#     '''
#     components = {}

#     def order_on_components(self, graph):
#         self._find_parents(graph)
#         self._find_children(graph)
#         print self.components.keys()
#         return self.components

#     def _find_parents(self, graph):
#         for layer, node in graph:
#             if isParent(node):
#                 self.components.setdefault((layer, node), [])

#     def _find_children(self, graph):
#         graph_copy = graph.copy()
#         for layer, node in graph_copy:
#             classified = False
#             if not isParent(node):
#                 for k in self.components.keys():
#                     if isinstance(k, tuple):
#                         l, p = k
#                         if check_parent_similarity(node, p):
#                             self.components[(l, p)].append((layer, node))
#                             classified = True
#                 if not classified:
#                     self.components.setdefault(node.referent, []).append((layer, node))


# class HtmlTree(HtmlConverter):
#     '''
#     Converts a Tree graph to HTML per layer or per component
#     '''
#     name = 'tree'
#     ordering = 'tree'

#     def convert_to_html(self):
#         # override
#         html = self.div([self.name], self.compile())
#         return html

#     def get_length(self):
#         return self.length

#     def convert_layer(self, nr):
#         nodes = self.get_layer(nr)
#         html = self.div(
#             ['layer l-' + str(nr)],
#             ''.join(node.convert_to_html() for node in nodes)
#             )
#         return html

#     def compile(self):
#         if self.ordering == 'tree':
#             return self.compile_as_tree()
#         elif self.ordering == 'components':
#             return self.compile_as_component()

#     def compile_as_tree(self):
#         layer_html = ''
#         for layer in range(self.get_length()+1):
#             layer_html += self.convert_layer(layer)
#         return layer_html

#     def convert_children(self, nodeTuples):
#         html = self.div(
#             ['child'],
#             ''.join(node.convert_with_extra(str(layer)) for layer, node in nodeTuples)
#             )
#         return html

#     def compile_as_component(self):
#         components = self.order_on_components(self.graph)
#         component_html = ''
#         for key, value in components.items():
#             if isinstance(key, tuple):
#                 layer, parent = key
#                 component_html += self.div(
#                     ['parent ' + parent.referent],
#                     parent.convert_with_extra(str(layer)) + self.convert_children(value)
#                     )
#             else:
#                 component_html += self.div(
#                     [key],
#                     self.convert_children(value)
#                     )
#         return component_html

