from typing import Annotated
from fastapi import Header

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    print(user_agent)
    return {"User-Agent": user_agent}



@app.get("/items2/")
async def read_items(strange_header: Annotated[str | None, Header(convert_underscores=False)] = None):
       return {"strange_header": strange_header}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
