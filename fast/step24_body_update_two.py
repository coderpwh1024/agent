from typing import Union

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



class Item(BaseModel):
    name:str
    description: Union[str,None]= None
    price: Union[float,None]= None
    tax: float=10.5
    tags: list[str]= []





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)