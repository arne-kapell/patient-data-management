import os


class PrefixMiddleware:
    def __init__(self, get_response, prefix="/"):
        self.get_response = get_response
        self.prefix = "/" if os.environ.get("DEBUG", 1) else "/pdm"

    def __call__(self, request):
        print(self.prefix)
        if not request.path.startswith(self.prefix):
            request.path = self.prefix + request.path
        response = self.get_response(request)
        # Code to be executed for each request/response after the view or other middleware is called.
        return response
