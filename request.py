import json


class AsyncRequest:
    Method: str
    URI: str
    HTTPVersion: str
    Headers: dict
    Body: str

    def __init__(self,):
        self.Method = ""
        self.URI = ""
        self.HTTPVersion = ""
        self.Headers = {}
        self.Body = ""

    @property
    def JSON(self, ):
        return json.loads(self.Body)
