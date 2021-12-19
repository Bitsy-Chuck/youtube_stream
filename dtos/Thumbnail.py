import json


class ThumbnailUrls:
    def __init__(self, default, medium, large):
        self.default = default
        self.medium = medium
        self.large = large

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
