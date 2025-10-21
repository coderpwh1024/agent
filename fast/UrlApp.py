import uvicorn
from fastapi import  FastAPI

app = FastAPI()

# python 中关于url路径
@app.get("/items/{item_id}")
async def read_item(item_id):
    print("item_id:",item_id)
    return {"item_id":item_id}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)