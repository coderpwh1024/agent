from typing import Union

import uvicorn
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: Union[str, None] = Cookie(default=None)):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q": query_or_default}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
