from typing import Annotated
import uvicorn
from fastapi import FastAPI, Path, Query

app = FastAPI()


# 元数据
@app.get("/items/{item_id}")
async def read_items(
        item_id: Annotated[int, Path(title="The ID of the item to get")],
        q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items2/{item_id}")
async def read_items2(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items3/{item_id}")
async def read_items3(*, q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items4/{item_id}")
async def read_items4(*, item_id: int = Path(title="The ID of the item to get", ge=10, le=200), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items5/{item_id}")
async def read_item5(*, item_id: int = Path(title="The ID of the item to get", ge=10, le=100), q: str,
                     size: float = Query(gt=0, lt=10.5)):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results





if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8001)
