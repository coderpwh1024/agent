import uvicorn
from fastapi import FastAPI
app = FastAPI()



@app.post("/items/",status_code=201)
async def create_item(name:str):
    return  {"name":name}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)