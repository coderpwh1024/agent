from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()



class Item(BaseModel):
    name:str
    description:str
    price:float
    tax:float | None = None



@app.put("/items/{item_id}")
async  def update_item(item_id:Annotated[int,Path(title="The ID of the item to get",ge=0,le=1000)],q:str|None=None,item:Item|None= None):
    results = {"item_id":item_id}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item})
    return  results




if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8001)
