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
        if "?" not in self.URI:
            return
        uri, parameters = self.URI.split("?")
        self.URI = uri

        if len(parameters) > 1:
            parameters = parameters.split("&")
            for query in parameters:
                if "=" in query:
                    key, value = query.split("=")
                    self.Parameters[key] = value
                else:
                    self.Parameters[key] = None

    @property
    def JSON(self, ):
        if self.Headers["Content-Type"] == "application/json":
            return json.loads(self.Body)
        return None
