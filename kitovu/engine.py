import requests
from .config import parse_config
from .utils import Paging
from .errors import ApiError


class Engine():
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
