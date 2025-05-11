from contextvars import ContextVar
from django.utils.deprecation import MiddlewareMixin
from .context import current_request

class CurrentUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        current_request.set(request)
        
    def process_exception(self, request, exception):
        current_request.set(None)

    def process_response(self, request, response):
        current_request.set(None)
        return response
