from typing import  Union
import uvicorn
from fastapi import FastAPI,Depends

app = FastAPI();


async  def common_parameters(q:Union[str,None]=None,skip:int=0,limit:int=100):
    return {"q":q,"skip":skip,"limit":limit}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)