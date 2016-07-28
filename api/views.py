import library
import notebooks
import texts
import gentext

from gentext.views.serializer import JsonView


MODELS = {
    'libraryauthor': gentext.models.bib.Author,
    'librarypublisher': gentext.models.bib.Publisher,
    'libraryitem': library.models.LibraryItem,
    'libraryexcerpt': library.models.LibraryExcerpt,
    'librarypage': library.models.LibraryPage,
    'librarycollection': library.models.LibraryCollection,
    'notebook': notebooks.models.Notebook,
    'notebookpage': notebooks.models.NotebookPage,
    'note': notebooks.models.Note,
    'novel': texts.models.Novel,
    'line': texts.models.Line,
    'chapter': texts.models.Chapter,
    'page': texts.models.Page,
    }


class API(JsonView):
    '''
    RESTful API for getting database information.
    Returns 400 entries from the database, distinguished
    by the 'part' url kwarg.

    request: model and (optional) primary key (pk)
    response: database access in JSON
    '''
    def process_request(self, request):
        # override
        model = request.GET.get('model')
        pk = request.GET.get('pk')
        part = request.GET.get('part') if request.GET.get('part') else 0
        return (model, pk, int(part))

    def exclude(self):
        '''
        Exclude image fields from the serialisation
        '''
        return ['image']

    def request_database(self, processed_data):
        '''
        Get items from the database according to the requested input.
        With this function, it is possible to filter which part of
        the data can be made available to the user.

        input: String model, according to constants
                String pk, primary key of item of interest
        output: QuerySet with items that match the request, or empty list
                if none matched.
        '''
        # override
        model, pk, part = processed_data
        items = []
        if pk:
            items = MODELS[model].objects.filter(pk=pk)
        else:
            pivot = 1000*part
            items = MODELS[model].objects.all()[pivot:pivot+1000]
        return items

    def get_claims(self):
        # override
        claim = {}
        claim['project'] = 'James Joyce Digital Library'
        claim['developed_at'] = 'Centre for Manuscript Genetics'
        claim['affiliation'] = 'University of Antwerp'
        claim['link'] = 'https://www.uantwerpen.be/en/rg/centre-for-manuscript-genetics/'
        return claim
