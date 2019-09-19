import json


class AsyncResponse:
    StatusCode: int
    Headers: dict
    Body: str

    def __init__(self, **kwargs):
        self.StatusCode = kwargs.get("status_code") or 204
        self.Headers = kwargs.get("headers") or {}
        self.Body = kwargs.get("body") or ""

    def set_header(self, k, v):
        self.Headers[k] = v

    def JSON(self, data: str):
        self.StatusCode = 200
        self.set_header("Content-type", "application/json")
        self.Body = json.dumps(data)

    def Text(self, data: str):
        self.StatusCode = 200
        self.set_header("Content-type", "text/plain")
        self.Body = data

    def Html(self, data: str):
        self.StatusCode = 200
        self.set_header("Content-type", "text/html")
        self.Body = data

    @property
    def __headers_serialized__(self, ):
        tmp = ""
        for k, v in self.Headers.items():
            tmp += '{}:{}\r\n'.format(k, v)
        return tmp

    def __toByes__(self,):
        return """HTTP/1.1 {}\r\n{}\r\n{}\r\n\r\n""".format(
            self.StatusCode,
            self.__headers_serialized__,
            self.Body,
        ).encode('utf-8')
