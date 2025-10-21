import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    print("item:", item)
    return "success"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
