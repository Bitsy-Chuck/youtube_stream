import json


class ApiKeyResponse:
    def __init__(self, id, api_key, consumed_quota, max_quota):
        self.id = id
        self.api_key = api_key
        self.consumed_quota = consumed_quota
        self.max_quota = max_quota

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
