from unittest import mock
from rest_framework.test import APIRequestFactory, force_authenticate


def api_test_request(method='get', data=None, user=None, view=None, query_string="", format="json", **kwargs):
    """
    Utility function used by the api's for unit tests.

    :param method:
    :param data:
    :param user:
    :param view:
    :param query_string:
    :param format:
    :param kwargs:
    :return:
    """

    _method = method
    if isinstance(method, dict):
        _method = list(method.keys())[0]

    factory = APIRequestFactory()
    if data:
        request = getattr(factory, _method)(path="", data=data, format=format, **kwargs)
    else:
        request = getattr(factory, _method)(query_string, **kwargs)

    request.session = mock.MagicMock()

    if user:
        force_authenticate(request, user=user)
    try:
        response = view.as_view()(request, **kwargs)
    except TypeError:
        response = view.as_view(method)(request, **kwargs)
    return response
