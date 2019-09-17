# asyncweb
async web framework wrote by python 3.7

## Example

```python
from asyncweb import AsyncRequest, AsyncRouter, AsyncWeb

def handler(req: AsyncRequest):
    print(req.__dict__)
    return


if __name__ == '__main__':
    r = AsyncRouter()

    r.POST("/", handler)

    web = AsyncWeb("localhost", 8000, r)
    web.Run()
```