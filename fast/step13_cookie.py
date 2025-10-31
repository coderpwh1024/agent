from typing import Annotated

import uvicorn
from fastapi import FastAPI,Cookie

app = FastAPI()


@app.get("/items/")
async  def read_items(ads_id:Annotated[str|None,Cookie()]=None):
    return {"ads_id": ads_id}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)