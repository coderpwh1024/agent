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



@app.post("/items/",response_model=Item,summary="Create an item",description="Create an item with all the information, name, description, price, tax and a set of unique tags")
async  def create_item(item: Item):
    return item





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
