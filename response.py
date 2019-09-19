import json
import time


class AsyncResponse:
    StatusCode: int
    Headers: dict
    Body: str
    __cookie__: dict
    __cookie_expire__: str

    def __init__(self, **kwargs):
        self.StatusCode = kwargs.get("status_code") or 204
        self.Headers = kwargs.get("headers") or {}
        self.Body = kwargs.get("body") or ""
        self.__cookie__ = {}
        self.__cookie_expire__ = None

    def set_header(self, k, v):
        self.Headers[k] = v

    def JSON(self, data):
        self.StatusCode = 200
        self.set_header("Content-Type", "application/json")
        self.Body = json.dumps(data)

    def Text(self, data: str):
        self.StatusCode = 200
        self.set_header("Content-Type", "text/plain")
        self.Body = data

    def Html(self, data: str):
        self.StatusCode = 200
        self.set_header("Content-Type", "text/html")
        self.Body = data

    def Redirect(self, path: str):
        self.StatusCode = 302
        self.set_header("Location", path)

    def SetCookie(self, key: str, val: str, expire_sec):
        self.__cookie__[key] = val
        expire = ""
        if expire_sec == None:
            expire = time.gmtime(time.time() + (24*60*60))
        else:
            expire = time.gmtime(time.time() + expire_sec)
        self.__cookie_expire__ = time.strftime("%a, %d-%b-%Y %T GMT", expire)

    def DelCookie(self, key: str):
        del self.__cookie__[key]

    @property
    def __headers_serialized__(self, ):
        tmp = ""
        for k, v in self.Headers.items():
            tmp += '{}:{}\r\n'.format(k, v)
        if len(self.__cookie__) > 0:
            cookies = ''
            for k, v in self.__cookie__.items():
                cookies += k+"="+v+";"
            tmp += 'Set-Cookie:{}'.format(cookies)
            tmp += 'Expires=' + self.__cookie_expire__
        return tmp

    def __toByes__(self,):
        return """HTTP/1.1 {}\r\n{}\r\n{}\r\n\r\n""".format(
            self.StatusCode,
            self.__headers_serialized__,
            self.Body,
        ).encode('utf-8')
