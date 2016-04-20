'''
Classes for conversion from Node/Tree/Branch object to X/HTML
'''
from django.utils.encoding import smart_str


class HtmlConverter(object):

    def div(self, classContent, divContent):
        html = '<div class="{0}">{1}</div>'.format(
            ' '.join(c for c in classContent),
            divContent
            )
        return html

    def get_html_content(self):
        pass

    def convert_to_html(self):
        pass


class HtmlNode(HtmlConverter):
    tag_content = []
    class_content = []
    image = '<span class="nodeIcon glyphicon glyphicon-record"></span>'

    def __init__(self):
        self.tag_content = ''
        self.class_content = []

    def convert_to_html(self):
        # override
        self.get_html_content()
        html = self.div(
            ['node', ' '.join(c for c in self.class_content)],
            self.image + self.div(
                ['nodeInfo'],
                self.build_content()
                )
            )
        return html

    def build_content(self):
        content = ''
        for i in range(len(self.tag_content)/2):
            content += self.div(
                [self.tag_content[2*i]],
                self.tag_content[2*i+1]
                )
        return content


class HtmlTree(HtmlConverter):
    '''
    Converts a Tree graph to HTML per layer or per component
    '''
    name = 'tree'

    def convert_to_html(self):
        # override
        html = self.div([self.name], self.compile())
        return html

    def get_length(self):
        return self.length

    def convert_layer(self, nr):
        nodes = self.get_layer(nr)
        html = self.div(
            ['layer layer-' + str(nr)],
            ''.join(node.convert_to_html() for node in nodes)
            )
        return html

    def compile(self):
        layer_html = ''
        for layer in range(self.get_length()+1):
            layer_html += self.convert_layer(layer)
        return layer_html


class HtmlBranch(HtmlTree):
    name = 'branch'

    def get_length(self):
        # override
        return len(self.graph)


# constants
LIBRARY_ITEM = 'libraryitem'
LIBRARY_EXCERPT = 'libraryexcerpt'
NOTEBOOKS_NOTEBOOK = 'notebook'
NOTEBOOKS_NOTE = 'note'


class DatabaseHtmlContent(object):
    '''
    Provides methods that returns database information/field reference
    '''
    @staticmethod
    def extract_html_fields(node):
        fields = [
            'nodename',
            node.name,
            'parentname',
            node.parent if node.parent else 'root'
            ]
        model = node.referent
        obj = node.pathObject
        if model == LIBRARY_ITEM:
            fields += [
                'type',
                'library item',
                'id',
                smart_str(obj.title),
                'author',
                smart_str(obj.get_authors()),
                'collection',
                obj.collection.title,
                'slug',
                obj.slug
                ]
        elif model == LIBRARY_EXCERPT:
            fields += [
                'type',
                'library excerpt',
                'id',
                obj,
                'content',
                smart_str(obj.content),
                'super',
                smart_str(obj.item.title)
                ]
        elif model == NOTEBOOKS_NOTEBOOK:
            fields += [
                'type',
                'notebook',
                'id',
                obj.name
                ]
        elif model == NOTEBOOKS_NOTE:
            fields += [
                'type',
                'note',
                'id',
                obj,
                'content',
                smart_str(obj.notejj),
                'super',
                obj.noteb.name
                ]
        return fields
