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

    def _get(self, url, **kwargs):
        r = requests.get(url, headers=self.headers, **kwargs)
        if not r.ok:
            raise ApiError(r.text)
        return r

    def _put(self, url, **kwargs):
        r = requests.put(url, headers=self.headers, **kwargs)
        if not r.ok:
            raise ApiError(r.text)
        return r

    def _delete(self, url, **kwargs):
        r = requests.delete(url, headers=self.headers, **kwargs)
        if not r.ok:
            raise ApiError(r.text)
        return r

    def get(self, uri, **kwargs):
        endpoint = self.hub + uri
        r = self._get(endpoint, **kwargs)
        while True:
            yield r
            paging = Paging(r.headers.get('link'))
            if paging.next_link:
                r = self._get(paging.next_link)
            else:
                break

    def put(self, uri, **kwargs):
        endpoint = self.hub + uri
        return self._put(endpoint, **kwargs)

    def delete(self, uri, **kwargs):
        endpoint = self.hub + uri
        return self._delete(endpoint, **kwargs)
