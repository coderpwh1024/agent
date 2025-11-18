import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI();

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
