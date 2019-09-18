# asyncweb
async web framework wrote by python 3.7

## Example

```python
from asyncweb import *


def get(req: AsyncRequest):
    return AsyncResponse(**{"status_code": 200, "body": "Hello World."})


def post(req: AsyncRequest):
    print(req.JSON)
    resp = AsyncResponse()
    resp.JSON({"Status": "ok"})
    return resp


if __name__ == "__main__":
    r = AsyncRouter()
    r.GET("/", get)
    r.POST("/", post)
    w = AsyncWeb("localhost", 8000, r)
    w.Run()

```