from django.views.generic import View
from django.http import JsonResponse
# from django.db.models.fields.related import ManyToManyField


def model_to_dict(instance):
    '''
    Serialize a model instance. ManyToManys are included.
    '''
    opts = instance._meta
    data = {}
    # for f in opts.concrete_fields + opts.many_to_many:
    #     if isinstance(f, ManyToManyField):
    #         if instance.pk is None:
    #             data[f.name] = []
    #         else:
    #             data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
    #     else:
    #         data[f.name] = unicode(f.value_from_object(instance))
    for f in opts.concrete_fields:
        data[f.name] = unicode(f.value_from_object(instance))
    return data


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

    def exclude(self):
        '''
        Returns list of fields that need to be excluded from the
        JSON serialisation.
        E.g. exclude all fields that has files!
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
            # include ManyToManys
            instance_dict = model_to_dict(item)
            itemDicts.append(instance_dict)

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
