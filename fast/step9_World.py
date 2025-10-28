# 在文件开头添加导入语句
import uvicorn
from fastapi import FastAPI
import asyncio

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
