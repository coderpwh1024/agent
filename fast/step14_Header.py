from email.header import Header
from typing import Annotated

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    print(user_agent)
    return {"User-Agent": user_agent}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
