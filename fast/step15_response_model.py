from typing import Any, Union, List

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


class UserIn(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    password: str
    full_name: str|None = None


class Item2(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    # "baz":{"name":"Baz","description":None,"price":50.2,"tax":10.5,"tags":[]}

    "baz": {
        "name": "Baz",
        "description": "The goes my baz",
        "price": 50.2,
        "tax": 10.5
    }
}


@app.post("/user2/", response_model=UserOut)
async def create_user2(user: UserIn) -> Any:
    return user;


@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn) -> UserIn:
    return user


@app.post("/items/", response_model=Item)
async def read_item(item: Item) -> Any:
    return item


@app.get("/items2/", response_model=list[Item])
async def read_items2() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 22.0}
    ]

@app.get("/items3/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item3(item_id: str):
    return items[item_id]


@app.get("/items4/{item_id}/name", response_model=Item2, response_model_exclude={"tax"})
async def read_item4(item_id: str):
    return items[item_id]


@app.get("/items5/{item_id}", response_model=Item2, response_model_include={"name", "description"})
async def read_item5(item_id: str):
    return items[item_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
