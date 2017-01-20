'''
Gathers database information via Django models.
'''
from django.utils.text import slugify

import library
import notebooks
import texts

# constants
LIBRARY_ITEM = 'libraryitem'
LIBRARY_PAGE = 'librarypage'
LIBRARY_EXCERPT = 'libraryexcerpt'
NOTEBOOKS_NOTEBOOK = 'notebook'
NOTEBOOKS_PAGE = 'notebookpage'
NOTEBOOKS_NOTE = 'note'
TEXTS_LINE = 'line'
TEXTS_PAGE = 'page'
TEXTS_CHAPTER = 'chapter'

MODELS = {
    LIBRARY_ITEM: library.models.LibraryItem,
    LIBRARY_EXCERPT: library.models.LibraryExcerpt,
    LIBRARY_PAGE: library.models.LibraryPage,
    NOTEBOOKS_NOTEBOOK: notebooks.models.Notebook,
    NOTEBOOKS_PAGE: notebooks.models.NotebookPage,
    NOTEBOOKS_NOTE: notebooks.models.Note,
    TEXTS_LINE: texts.models.Line,
    TEXTS_PAGE: texts.models.Page,
    TEXTS_CHAPTER: texts.models.Chapter
    }

DOWN_LIMIT = LIBRARY_ITEM
UP_LIMIT = TEXTS_CHAPTER


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
                'Object cannot be decided from input "{}"!'.format(modelObjs)
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

        try:
            pk = int(node.name)
            return MODELS[model].objects.filter(pk=pk)
        except ValueError:
            if model in [LIBRARY_PAGE, NOTEBOOKS_PAGE, TEXTS_PAGE, NOTEBOOKS_NOTEBOOK, TEXTS_CHAPTER]:
                return MODELS[model].objects.filter(slug=slugify(node))
            elif model == LIBRARY_ITEM:
                return MODELS[model].objects.filter(slug__icontains=slugify(node))
            elif model == LIBRARY_EXCERPT:
                return MODELS[model].objects.filter(content__icontains=node)
            elif model == NOTEBOOKS_NOTE:
                return MODELS[model].objects.filter(notejj__icontains=node)
            elif model == TEXTS_LINE:
                return MODELS[model].objects.filter(content__icontains=node)

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
        # perform shallow query based on current object
        if downstream:
            if not (model == DOWN_LIMIT and bool(parents)):
                q += self.query_downstream(modelObj, model)
        if upstream:
            if not (model == UP_LIMIT and bool(parents)):
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
            q = modelObj.page_set.filter(excerpt_set__isnull=False)
        elif model == LIBRARY_PAGE:
            q = modelObj.excerpt_set.filter(note_set__isnull=False)
        elif model == LIBRARY_EXCERPT:
            q = modelObj.note_set.all()
        elif model == NOTEBOOKS_NOTE:
            if modelObj.note:
                q = [modelObj.note]
            elif modelObj.textline:
                q = [modelObj.textline]
            else:
                []
        elif model == NOTEBOOKS_PAGE:
            q = modelObj.note_set.all()
        elif model == TEXTS_LINE:
            q = [modelObj.chapter] if modelObj.chapter else []
        elif model == TEXTS_PAGE:
            q = [modelObj.chapter] if modelObj.chapter else []
        return list(q)

    def query_upstream(self, modelObj, model):
        '''Performs ForeignKey/ManyToMany query counterclockwise'''
        q = []
        if model == LIBRARY_PAGE:
            q = [modelObj.item]
        elif model == LIBRARY_EXCERPT:
            q = [modelObj.page]
        elif model == NOTEBOOKS_NOTEBOOK:
            q = modelObj.libraryitem.all()
        elif model == NOTEBOOKS_NOTE:
            q = modelObj.libraryexcerpt.all()
        elif model == TEXTS_PAGE:
            q = modelObj.line_set.filter(note_set__isnull=False)
        elif model == TEXTS_LINE:
            q = modelObj.note_set.all()
        elif model == TEXTS_CHAPTER:
            q = modelObj.page_set.all()
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
