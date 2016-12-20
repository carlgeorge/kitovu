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
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = 'token {}'.format(token)

    def get(self, uri, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        return ok(requests.get(endpoint, **kwargs))

    def get_all(self, uri, **kwargs):
        r = self.get(uri, **kwargs)
        while True:
            yield r
            paging = Paging(r.headers.get('link'))
            if paging.next_link:
                r = ok(requests.get(paging.next_link, headers=self.headers))
            else:
                break

    def post(self, uri, payload, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        kwargs['json'] = payload
        return ok(requests.post(endpoint, **kwargs))

    def put(self, uri, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        return ok(requests.put(endpoint, **kwargs))

    def delete(self, uri, **kwargs):
        endpoint = self.hub + uri
        kwargs['headers'] = self.headers
        return ok(requests.delete(endpoint, **kwargs))
