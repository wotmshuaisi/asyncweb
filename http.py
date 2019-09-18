from .router import AsyncRouter
from .request import AsyncRequest
from .response import AsyncResponse

import socket
import asyncio
import time


class AsyncWeb:
    __internal_loop__: asyncio.AbstractEventLoop = None
    __socket_server__: socket.socket = None
    __router_obj__: AsyncRouter
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
        if int(req.Headers.get("Content-Length")) != 0:
            data_length = int(req.Headers["Content-Length"])
            for x in range((data_length//1024)+1):
                body += await self.__internal_loop__.sock_recv(client, 1024)

        req.Body = body

        if self.__router_obj__[req.Method+"_"+req.URI] == None:
            await self.__internal_loop__.sock_sendall(client, AsyncResponse(**{"status_code": 404, "body": "404 Not Found."}).__toByes__())
            client.close()
            return

        response: AsyncResponse = self.__router_obj__[
            req.Method+"_"+req.URI](req)

        if response != None:
            await self.__internal_loop__.sock_sendall(client, response.__toByes__())

        client.close()

    async def __event_loop__(self,):
        while True:
            client, _ = await self.__internal_loop__.sock_accept(self.__socket_server__)
            self.__internal_loop__.create_task(self.__socket_handler__(client))

    def Run(self, ):
        print("====> Listening on [{}:{}]".format(self.host, self.port))
        for uri in self.__router_obj__:
            print("====> {}".format(uri))

        self.__internal_loop__ = asyncio.get_event_loop()
        self.__internal_loop__.run_until_complete(self.__event_loop__())
