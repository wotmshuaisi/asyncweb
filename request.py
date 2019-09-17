import json
import socket


class AsyncRequest:
    Connection: socket.socket
    Method: str
    URI: str
    HTTPVersion: str
    Headers: dict
    Body: str

    def __init__(self, conn: socket.socket):
        self.Connection = conn
        self.Method = ""
        self.URI = ""
        self.HTTPVersion = ""
        self.Headers = {}
        self.Body = ""

    @property
    def JSON(self, ):
        return json.loads(self.Body)
