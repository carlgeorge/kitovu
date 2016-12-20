import functools
import requests
from .config import load_profile, load_config
from .utils import Paging


def ok(response):
    if response.ok:
        return response
    else:
        raise SystemExit(response.json()['message'])


class Api():
    def __init__(self, profile=None, config=None):
        if profile and config:
            raise SystemExit('use either profile or config, not both')
        elif profile:
            self.hub, token = load_profile(profile)
        elif config:
            self.hub, token = load_config(config)
        else:
            self.hub, token = None, None
        if self.hub is None:
            self.hub = 'https://api.github.com'
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            headers['Authorization'] = 'token {}'.format(token)
        self._get = functools.partial(requests.get, headers=headers)
        self._put = functools.partial(requests.put, headers=headers)
        self._post = functools.partial(requests.post, headers=headers)
        self._delete = functools.partial(requests.delete, headers=headers)

    def get(self, uri):
        return ok(self._get(self.hub + uri))

    def get_all(self, uri):
        r = self.get(uri)
        while True:
            yield r
            paging = Paging(r.headers.get('link'))
            if paging.next_link:
                r = ok(self._get(paging.next_link))
            else:
                break

    def post(self, uri, payload):
        return ok(self._post(self.hub + uri, json=payload))

    def put(self, uri):
        return ok(self._put(self.hub + uri))

    def delete(self, uri):
        return ok(self._delete(self.hub + uri))
