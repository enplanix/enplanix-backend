import re
from django.http import JsonResponse

class AxiosOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        self.exempt_paths = [
            re.compile(rf'^/api/upload/images/{uuid_pattern}/content/?$'),
            re.compile(rf'^/api/upload/files/{uuid_pattern}/content/?$'),
        ]

    def __call__(self, request):
        path = request.path
        if any(pattern.match(path) for pattern in self.exempt_paths):
            return self.get_response(request)

        if path.startswith('/api/'):
            accept_header = request.headers.get('Accept', '')
            if 'application/json' not in accept_header or 'text/plain' not in accept_header:
                return JsonResponse({'detail': 'Access to this API is restricted'}, status=403)

        return self.get_response(request)
