'''
Gathers database information via Django models.
'''
from django.utils.text import slugify

from library.models import LibraryItem, LibraryExcerpt
from notebooks.models import Notebook, Note


# constants
LIBRARY_ITEM = 'libraryitem'
LIBRARY_EXCERPT = 'libraryexcerpt'
NOTEBOOKS_NOTEBOOK = 'notebook'
NOTEBOOKS_NOTE = 'note'

UPPER_LIMIT = LIBRARY_ITEM
LOWER_LIMIT = ''


class DatabaseQuery(object):
    '''
    Provides query methods for nodes
    '''
    def get(self, node, model=''):
        '''
        Get Query object from Node object

        input: a Node object
        output: Database object that matched the node name
        '''
        modelObjs = self.filter(node, target_model=model)
        if len(modelObjs) != 1:
            raise IOError(
                'Get method cannot decide on this input: {}!'.format(modelObjs)
                )
        else:
            return modelObjs.first()

    def filter(self, node, target_model=''):
        '''
        Returns database object from Node input

        input: Node object
        output: QuerySet that matched the node name
        '''
        model = target_model if target_model else node.referent
        if model == LIBRARY_ITEM:
            return LibraryItem.objects.filter(slug__icontains=slugify(node))
        elif model == LIBRARY_EXCERPT:
            return LibraryExcerpt.objects.filter(content__icontains=node)
        elif model == NOTEBOOKS_NOTEBOOK:
            return Notebook.objects.filter(slug=slugify(node))
        elif model == NOTEBOOKS_NOTE:
            return Note.objects.filter(notejj__icontains=node)

    def query(self, node, downstream=False, upstream=False):
        '''
        Perform a query with 1 constraint through the database in
        downstream and/or upstream movement.
        If the input Node has a parent, it also performs a query with
        2 constraints, or a 'deep' query.

        input: Node object
        output: QuerySet or empty list
        '''
        modelObj = node.dbObject
        model = node.referent
        parents = node.parent
        q = []
        # perform naive shallow query based on current object
        if downstream:
            q += self.query_downstream(modelObj, model)
        elif upstream:
            q += self.query_upstream(modelObj, model)
        if parents:
            for parent in parents:
                # perform deep query using parent object
                q += self.deep_query(modelObj, model, parent)
        return q

    def query_downstream(self, modelObj, model):
        '''Performs ForeignKey/ManyToMany query clockwise'''
        q = []
        if model == LIBRARY_ITEM:
            q = modelObj.excerpt_set.all()
        elif model == LIBRARY_EXCERPT:
            q = modelObj.note_set.all()
        return list(q)

    def query_upstream(self, modelObj, model):
        '''Performs ForeignKey/ManyToMany query counterclockwise'''
        q = []
        if model == LIBRARY_EXCERPT:
            q = [modelObj.item]
        elif model == NOTEBOOKS_NOTEBOOK:
            q = modelObj.libraryitem.all()
        elif model == NOTEBOOKS_NOTE:
            q = modelObj.libraryexcerpt.all()
        return list(q)

    def deep_query(self, modelObj, model, parentNode):
        '''
        Perform query with multiple constraints

        input: database model object
                String model name
                Node object parent
        output: list with matches (converted QuerySet)
        '''
        q = []
        parentRef = parentNode.referent
        parentObj = parentNode.dbObject
        if model == LIBRARY_ITEM:
            if parentRef == NOTEBOOKS_NOTEBOOK:
                q = modelObj.excerpt_set.filter(note_set__noteb=parentObj)
        elif model == NOTEBOOKS_NOTEBOOK:
            if parentRef == LIBRARY_ITEM:
                q = modelObj.note_set.filter(libraryexcerpt__item=parentObj)
        return list(q)
