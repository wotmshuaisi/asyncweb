import json


class AsyncRequest:
    Method: str
    URI: str
    HTTPVersion: str
    Headers: dict
    Body: str

    def __init__(self):
        self.Method = ""
        self.URI = ""
        self.HTTPVersion = ""
        self.Headers = {}
        self.Body = ""

    @property
    def JSON(self, ):
        if self.Headers["Content-Type"] == "application/json":
            return json.loads(self.Body)
        return None
