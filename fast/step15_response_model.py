from typing import Any

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/",response_model= Item)
async def read_item(item: Item) -> Any:
    return item

@app.get("/items2/",response_model=list[Item])
async  def read_items2()->Any:
    return [
        {"name":"Portal Gun","price":42.0},
        {"name":"Plumbus","price":22.0}
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
