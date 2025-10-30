from typing import Union

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: list = []


class Item2(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []


class Item3(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Item4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    # images: Image | None = None
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item4]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Item3):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items4/{item_id}")
async def update_item4(item_id: int, item: Item4):
    result = {"item_id": item_id, "item": item}
    return result



@app.put("/images")
async  def create_multiple_images(images: list[Image]):
    for image in images:
        print(image.url)
        print(image.name)
    return  images



@app.put("/offers")
async def update_item5(offer: Offer):
    return offer;


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
