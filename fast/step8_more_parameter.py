from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
                      q: str | None = None, item: Item | None = None):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.put("/items3/{item_id}")
async def update_item3(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.put("/items4/{item_id}")
async def update_item4(*, item_id: int, item: Item, user: User, importance: Annotated[int, Body(gt=0)],
                       q: str | None = None, ):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.put("/items5/{item_id}")
async  def update_item5(item_id:int,item:Annotated[Item,Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results



if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8001)
