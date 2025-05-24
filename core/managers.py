from django.db import models


class UserFilterMixin:
    user_field = 'user'

    def __init__(self, user_field=None):
        self.user_field = user_field or self.user_field

    def _from_user(self, user=None):
        if not user:
            return self.none()
        filter_kwargs = {self.user_field: user}
        return self.filter(**filter_kwargs)

    def from_user(self, user):
        return self._from_user(user)

    def from_request_user(self, request):
        try:
            user = request.user
        except AttributeError:
            return self.none()
        return self._from_user(user)


class BusinessFilterMixin:
    business_field = 'business'

    def __init__(self, business_field=None):
        self.business_field = business_field or self.business_field

    def _within_business(self, business=None):
        if not business:
            return self.none()
        filter_kwargs = {self.business_field: business}
        return self.filter(**filter_kwargs)

    def within_business(self, business):
        return self._within_business(business)

    def within_request_business(self, request):
        try:
            business = request.user.preference.current_business
        except AttributeError:
            return self.none()
        return self._within_business(business)


class CustomManager(BusinessFilterMixin, UserFilterMixin, models.Manager):
    def __init__(self, business_field=None, user_field=None):
        models.Manager.__init__(self)
        BusinessFilterMixin.__init__(self, business_field)
        UserFilterMixin.__init__(self, user_field)

