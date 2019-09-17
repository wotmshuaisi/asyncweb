class AsyncRouter(object):
    __table__: dict

    def __init__(self):
        self.__table__ = {}

    def GET(self, uri, func):
        self.__table__["GET_"+uri] = func

    def POST(self, uri, func):
        self.__table__["POST_"+uri] = func

    def PUT(self, uri, func):
        self.__table__["PUT_"+uri] = func

    def DELETE(self, uri, func):
        self.__table__["DELETE_"+uri] = func

    def __getitem__(self, name):
        if name in self.__table__:
            return self.__table__[name]
        return None
