from typing import Literal, Annotated

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# 参数模型
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "update_at"] = "create_at"
    tags: list[str] = []


# 参数模型，过滤不必要参数
class FilterParams2(BaseModel):
    model_config ={"extra":"forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int=Field(0,ge=0)
    order_by: Literal["created_at", "update_at"] = "create_at"
    tags: list[str] = []




@app.get("/items")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


@app.get("/items2")
async  def read_items2(filter_query: Annotated[FilterParams2, Query()]):
    return  filter_query



if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8001)
