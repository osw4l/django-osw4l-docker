import json

import requests
from django.core.exceptions import ImproperlyConfigured


class FCMMessage(object):
    def __init__(self):
        from .settings import API_KEY, MAX_RECIPIENTS, API_URL
        self.api_key = API_KEY
        self.api_url = API_URL
        self.max_recipients = MAX_RECIPIENTS
        if not self.api_key:
            raise ImproperlyConfigured(
                "You haven't set the DRF_FCM 'API_KEY' in settings.py.")

    def __chunks(self, items, limit):

        for i in range(0, len(items), limit):
            yield items[i:i + limit]

    def send(self, registration_ids, **kwargs):
        if isinstance(registration_ids, str):
            return self.__notify(registration_ids, **kwargs)

        if len(registration_ids) > self.max_recipients:
            for ids in self.__chunks(registration_ids, self.max_recipients):
                return self.__notify(ids, **kwargs)
        else:
            return self.__notify(registration_ids, **kwargs)

    def __notify(self, to, **kwargs):
        headers = {'content-type': 'application/json',
                   'Authorization': 'key=' + self.api_key}
        if isinstance(to, list):
            kwargs['registration_ids'] = to
        if isinstance(to, str):
            kwargs['to'] = to

        response = requests.post(self.api_url, data=json.dumps(kwargs),
                                 headers=headers)
        return response
