import json


class AsyncRequest:
    Method: str
    URI: str
    Parameters: dict
    HTTPVersion: str
    Headers: dict
    Body: str

    def __init__(self):
        self.Method = ""
        self.URI = ""
        self.Parameters = {}
        self.HTTPVersion = ""
        self.Headers = {}
        self.Body = ""

    def __parameters_parse__(self, ):
        uri, parameters = self.URI.split("?")
        self.URI = uri
        parameters = parameters.split("&")
        for query in parameters:
            key, value = query.split("=")
            self.Parameters[key] = value

    @property
    def JSON(self, ):
        if self.Headers["Content-Type"] == "application/json":
            return json.loads(self.Body)
        return None
