class Paging():
    def __init__(self, raw):
        self.next_link = None
        self.prev_link = None
        self.last_link = None
        self.first_link = None
        if raw is not None:
            links = raw.split(', ')
            for link in links:
                url, name = link.split('; ')
                url = url.strip('<>')
                if name == 'rel="next"':
                    self.next_link = url
                if name == 'rel="last"':
                    self.last_link = url
                if name == 'rel="first"':
                    self.first_link = url
                if name == 'rel="prev"':
                    self.prev_link = url


