import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 必选参数查询
@app.post("/items/")
async def create_item(item: Item):
    print("item:", item)
    return "success"


# 编辑与新增参数等
@app.post("/items2/")
async def create_item2(item: Item):
    print("item:", item)
    item_dict = item.dict()
    if item_dict is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 带有路径的参数
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    print("item_id:", item_id)
    return {"item_id": item_id, **item.dict()}


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
