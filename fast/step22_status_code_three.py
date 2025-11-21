import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items")
async def read_item():
    return [{"name": "Foo", "price": 42}]


@app.get("/users", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elements", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
