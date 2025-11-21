from typing import Union, Set
import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    # tags:list[str]=set()
    tags: Set[str] = set()


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item


@app.post("/items2", response_model=Item, tags=["items"])
async def create_item2(item: Item):
    return item


@app.get("/item3", tags=["items"])
async  def read_items():
    return {"name": "Foo", "price": 42}



@app.get("/users", tags=["users"])
async  def read_users():
    return [{"username":"johndoe"}]




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
