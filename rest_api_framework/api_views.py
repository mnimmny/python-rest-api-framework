import json
from base import JsonResponse
from werkzeug.exceptions import BadRequest
from werkzeug.wrappers import Request


class WSGIWrapper(object):
    """
    accept a request, return a response
    """
    def __call__(self, environ, start_response):
        """
        return the wsgi wrapper
        """
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)


class ApiView(WSGIWrapper):
    """
    Handle the basic functionality of a Restful API
    """
    def index(self, request):
        """
        The root url of your ressources. Should present a list of
        ressources if method is GET.
        Should create a ressource if method is POST
        """
        if request.method == "GET":
            return self.get_list(request)

        if request.method == "POST":
            return self.create(request)

    def paginate(self, request):
        """
        A pagination example. Feel free to implement your own
        """
        first_id = request.values.to_dict().get("first_id", 0)
        filters = request.values.to_dict()
        filters.pop("first_id", None)
        return JsonResponse(
            json.dumps(
                self.datastore.get_list(start=first_id, **filters)),
            status=200)

    def get_list(self, request):
        return self.paginate(request)

    def unique_uri(self, request, identifier):
        """
        Retreive a unique object with his URI.
        Act on it accordingly to the Http verb used.
        """
        if request.method == "GET":
            return self.get(request, identifier)
        if request.method == "PUT":
            return self.update(request, identifier)
        if request.method == "DELETE":
            return self.delete(request, identifier)

    def get(self, request, identifier):
        """
        Return an object or 404
        """
        obj = self.datastore.get(identifier=identifier)

        return JsonResponse(
            json.dumps(obj),
            status=200)

    def create(self, request):
        """
        Create a new object in the datastore
        """
        print request.data
        try:
            data = json.loads(request.data)
        except:
            raise BadRequest()
        response = self.datastore.create(data)
        return JsonResponse(headers={"location": str(response)}, status=201)

    def update(self, request, identifier):
        """
        Update an object in the datastore
        """
        obj = self.datastore.get(identifier=identifier)
        obj = self.datastore.update(obj, json.loads(request.data))
        return JsonResponse(
            json.dumps(obj),
            status=200)

    def delete(self, request, identifier):
        obj = self.datastore.delete(identifier=identifier)
        return JsonResponse("Hello", status=200)