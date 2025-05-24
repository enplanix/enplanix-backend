from rest_framework.exceptions import PermissionDenied

class BusinessViewMixin:
    def get_request_business(self):
        try:
            return self.request.user.preference.current_business
        except AttributeError:
            return None