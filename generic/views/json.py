from django.views.generic import View
from django.http import JsonResponse


class JsonView(View):
    '''
    Very basic view to provide parts of the database in JSON format.
    This is useful to distribute the data and to offer possibilities
    for further applications of the same data.
    This class is far from usable as-is. The actual content of the JSON
    should be accessable from a child class.

    returns: JsonResponse of database fields
    '''

    def get_claims(self):
        '''
        Get information of the rightful creators/owners

        Should be overridden.
        '''
        return {}

    def process_request(self, request):
        '''
        Get the relevant information from the request.

        Should be overridden.
        '''
        return []

    def request_database(self, processed_request):
        '''
        Get items from the database according to the requested input.
        With this function, it is possible to filter which part of
        the data can be made available to the user.
        '''
        return []

    def jsonify(self, items):
        '''
        Jsonify the database items.
        Get every field into a dict.

        input: a list/QuerySet of database items
        output: the same list as a dictionary, ready
                to be exported as JSON
        '''
        itemDicts = []

        for item in items:
            json = {}
            for k, v in item.__dict__.iteritems():
                json[k] = v
            del json['_state']
            itemDicts.append(json)

        return {
            'items': itemDicts,
            'project_info': self.get_claims()
            }

    def get(self, request, *args, **kwargs):
        '''
        Perform the response. First, process the request. Then,
        get the appropriate items from the database according
        to the request. Finally, return the response as JSON.

        output: JsonResponse of matching database items
        '''
        processed_request = self.process_request(request)
        items = self.request_database(processed_request)
        return JsonResponse(self.jsonify(items))
