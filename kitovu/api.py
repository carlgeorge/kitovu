import requests
from .config import load_profile, load_config
from .utils import Paging
from .errors import KitovuError


class Api():
    def __init__(self, profile=None, config=None):
        if profile:
            self.hub, self.token = load_profile(profile)
        elif config:
            self.hub, self.token = load_config(config)
        else:
            raise KitovuError('requires either a profile name or a path to a '
                              'config file')
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'Authorization': 'token {}'.format(self.token)}

    def check(self, response):
        if not response.ok:
            raise KitovuError(response.text)
        return response

    def get(self, uri, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        return self.check(requests.get(endpoint, **kwargs))

    def get_all(self, uri, **kwargs):
        r = self.get(uri, **kwargs)
        while True:
            yield r
            paging = Paging(r.headers.get('link'))
            if paging.next_link:
                r = self.check(requests.get(paging.next_link,
                                            headers=self.headers))
            else:
                break

    def post(self, uri, payload, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        kwargs['json'] = payload
        return self.check(requests.post(endpoint, **kwargs))

    def put(self, uri, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        return self.check(requests.put(endpoint, **kwargs))

    def delete(self, uri, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        return self.check(requests.delete(endpoint, **kwargs))
