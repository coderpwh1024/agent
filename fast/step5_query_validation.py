from typing import Union

import uvicorn
from fastapi import FastAPI,Query

app = FastAPI()


@app.get("/items/")
async def read_item(q: str | None = None):
    results = {"item": [{"itme_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



@app.get("/items2/")
async  def read_item2(q:Union[str,None]=Query(default= None,max_length=50)):
    results = {"items":[{"item_id":"Foo"},{"item_id":"Bar"}]}
    if q:
        results.update({"q":q})
    return  results






if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8001)
