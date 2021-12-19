import json

class Thumbnail:
    def __init__(self, default_url, medium_url, large_url):
        self.default_url = default_url
        self.medium_url = medium_url
        self.large_url = large_url

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
