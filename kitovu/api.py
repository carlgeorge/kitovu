import requests
from .config import parse_config
from .utils import Paging
from .errors import ApiError


class Api():
    def __init__(self, profile):
        self.profile = profile
        self.hub, self.user, self.token = parse_config(profile)
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'Authorization': 'token {}'.format(self.token)}

    def _call(self, verb, url, **kwargs):
        if verb == 'get':
            r = requests.get(url, headers=self.headers, **kwargs)
        elif verb == 'head':
            r = requests.head(url, headers=self.headers, **kwargs)
        elif verb == 'put':
            r = requests.put(url, headers=self.headers, **kwargs)
        elif verb == 'post':
            r = requests.post(url, headers=self.headers, **kwargs)
        elif verb == 'delete':
            r = requests.delete(url, headers=self.headers, **kwargs)
        elif verb == 'patch':
            r = requests.patch(url, headers=self.headers, **kwargs)
        else:
            msg = 'the verb {} has not yet been implemented'
            raise SystemExit(msg.format(verb))
        if not r.ok:
            raise ApiError(r.text)
        return r

    def get(self, uri, **kwargs):
        endpoint = self.hub + uri
        r = self._call('get', endpoint, **kwargs)
        while True:
            yield r
            paging = Paging(r.headers.get('link'))
            if paging.next_link:
                r = self._call('get', paging.next_link)
            else:
                break

    def put(self, uri, **kwargs):
        endpoint = self.hub + uri
        return self._call('put', endpoint, **kwargs)

    def delete(self, uri, **kwargs):
        endpoint = self.hub + uri
        return self._call('delete', endpoint, **kwargs)
