from .router import AsyncRouter
from .request import AsyncRequest
from .response import AsyncResponse

import logging
import asyncio
import socket
import time
import sys


class AsyncWeb:
    __internal_loop__: asyncio.AbstractEventLoop = None
    __socket_server__: socket.socket = None
    __router_obj__: AsyncRouter
    logger: logging.Logger
    host: str
    port: int

    def __init__(self, host: str, port: int, router: AsyncRouter):
        self.__socket_server__ = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_server__.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket_server__.bind((host, port))
        self.__socket_server__.setblocking(False)
        self.__socket_server__.listen(12)
        self.__router_obj__ = router

        self.host, self.port = host, port

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '[%(levelname)s]%(asctime)s: %(message)s'))
        self.logger.addHandler(handler)

    async def __socket_handler__(self, client: socket.socket):
        headers = b''
        while True:
            headers += await self.__internal_loop__.sock_recv(client, 1)
            if headers[-4:] == b'\r\n\r\n':
                headers = headers[:-4]
                break

        headers = headers.decode('utf-8')
        headers = headers.split("\r\n")

        req = AsyncRequest()
        for x in range(len(headers)):
            if x == 0:
                req.Method, req.URI, req.HTTPVersion = headers[x].split(" ")
                continue
            h = headers[x].split(": ")
            req.Headers[h[0]] = h[1]

        body: bytes = b''
        if req.Headers.get("Content-Length") != None and int(req.Headers.get("Content-Length")) != 0:
            data_length = int(req.Headers["Content-Length"])
            for x in range((data_length//1024)+1):
                body += await self.__internal_loop__.sock_recv(client, 1024)

        req.Body = body

        if self.__router_obj__[req.Method+"_"+req.URI] == None:
            await self.__internal_loop__.sock_sendall(client, AsyncResponse(**{"status_code": 404, "body": "404 Not Found."}).__toByes__())
            client.close()
            self.__http_log__(logging.WARNING, req.Method, 404,
                              req.URI, req.Headers.get("Content-Length"), req.Headers.get("User-Agent"))
            return

        response: AsyncResponse = self.__router_obj__[
            req.Method+"_"+req.URI](req)

        if response != None:
            await self.__internal_loop__.sock_sendall(client, response.__toByes__())
            level = logging.INFO
            if response.StatusCode > 300 and response.StatusCode < 199:
                level = logging.WARNING
            self.__http_log__(level, req.Method, response.StatusCode,
                              req.URI, req.Headers.get("Content-Length"), req.Headers.get("User-Agent"))
        else:
            self.__http_log__(logging.error, req.Method, None,
                              req.URI, req.Headers.get("Content-Length"), req.Headers.get("User-Agent"))

        client.close()

    async def __event_loop__(self,):
        while True:
            client, _ = await self.__internal_loop__.sock_accept(self.__socket_server__)
            self.__internal_loop__.create_task(self.__socket_handler__(client))

    def __http_log__(self, level: str, method: str, status_code: int, path: str, reqlength: str, user_agent: str):
        fn = None
        if level == logging.WARNING:
            fn = self.logger.warning
        if level == logging.INFO:
            fn = self.logger.info
        if level == logging.ERROR:
            fn = self.logger.error
        fn("[Method: {}] [Status: {}] [Path: {}] [Length: {}] [Agent: {}]".format(
            method, status_code, path, reqlength, user_agent))

    def Run(self, ):
        print("====> Listening on [{}:{}]".format(self.host, self.port))
        for uri in self.__router_obj__:
            print("====> {}".format(uri))

        self.__internal_loop__ = asyncio.get_event_loop()
        self.__internal_loop__.run_until_complete(self.__event_loop__())
