import uvicorn
from fastapi import FastAPI

app = FastAPI()

fake_items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 设置默认值等
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    print("skip:", skip, "limit:", limit)
    return fake_items[skip: skip + limit]


# 查询参数类型状态

# @app.get("/items/{item_id}")
# async  def read_item(item_id:str,q:str|None=None,short:bool=False):
#     item = {"item_id":item_id}
#     print("item_id:",item_id)
#     print("q:",q)
#     print("short:",short)
#     if q:
#         item.update({"q":q})
#         print("q:",q)
#     if not short:
#         item.update(
#             {"description":"This is an amazing item that has a long description"}
#         )
#     return  item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}

    if q:
        item.update({"q": q})
        print("q:", q)
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 必选参数查询

# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     print("item_id:", item_id)
#     print("needy:", needy)
#     item = {"item_id": item_id, "needy": needy}
#     return item


@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int | None = None):
    print("item_id:", item_id, "needy:", needy, "skip:", skip, "limit:", limit)
    item = {"item": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8001)
