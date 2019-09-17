from .router import AsyncRouter
from .request import AsyncRequest

import socket
import asyncio


class AsyncWeb:
    __internal_loop__: asyncio.AbstractEventLoop = None
    __socket_server__: socket.socket = None
    __router_obj__: AsyncRouter

    def __init__(self, host: str, port: int, router: AsyncRouter):
        self.__socket_server__ = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_server__.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket_server__.bind((host, port))
        self.__socket_server__.setblocking(False)
        self.__socket_server__.listen(12)
        self.__router_obj__ = router

    async def __socket_handler__(self, client: socket.socket):
        req = await self.__internal_loop__.sock_recv(client, 500)
        headers, body = req.decode('utf-8').split("\r\n\r\n")
        headers = headers.split("\r\n")

        req = AsyncRequest()
        req.Body = body

        for x in range(len(headers)):
            if x == 0:
                req.Method, req.URI, req.HTTPVersion = headers[x].split(" ")
                continue
            h = headers[x].split(": ")
            req.Headers[h[0]] = h[1]

        if self.__router_obj__[req.Method+"_"+req.URI] == None:
            client.close()
            return
        self.__router_obj__[req.Method+"_"+req.URI](req)

        client.close()

    async def __event_loop__(self,):
        while True:
            client, _ = await self.__internal_loop__.sock_accept(self.__socket_server__)
            self.__internal_loop__.create_task(self.__socket_handler__(client))

    def Run(self, ):
        self.__internal_loop__ = asyncio.get_event_loop()
        self.__internal_loop__.run_until_complete(self.__event_loop__())
