from typing import Union, Set

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, summary="Create an item",
          description="Create an item with all the information, name, description, price, tax and a set of unique tags")
async def create_item(item: Item):
    return item


@app.post("/items2", response_model=Item, summary="Create an items")
async def create_item2(item: Item):
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
