from typing import Union
import uvicorn
from fastapi import FastAPI,status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    description:Union[str,None]=None
    price:float
    tax:Union[float,None]=None
    tags:list[str]=set()




@app.post("/items",response_model= Item,status_code=status.HTTP_201_CREATED)
async  def create_item(item:Item):
    return item




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)