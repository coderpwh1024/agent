import uvicorn
from fastapi import  FastAPI

app = FastAPI()

# python 中关于url路径
# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     print("item_id:",item_id)
#     return {"item_id":item_id}


@app.get("/items/{item_id}")
async  def read_item(item_id:str):
    print("item_id:",item_id)
    return {"item_id":item_id}



from enum import  Enum

# 枚举
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async  def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name":model_name,"message":"Deep Learning FTW"}

    if model_name.value== "lenet":
        return {"model_name":model_name,"message":"LeCNN all the images"}

    return {"model_name":model_name,"message":"Have some residuals"}

# 上传文件路径
@app.get("/files/{file_path:path}")
async  def read_file(file_path:str):
    print("file_path:",file_path)
    return {"file_path":file_path}






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)