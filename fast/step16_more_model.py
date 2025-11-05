from typing import Union
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


class Item(BaseModel):
    name: str
    description: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


def BaseItem(BaseModel):
    description: str | None = None
    type: str


def CarItem(BaseItem):
    type: str = "car"
    size: int


def PlaneItem(BaseItem):
    type: str = "plane"
    size: int





items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "items2": {
        "description": "Music is my aeroplane,it's my aeroplan",
        "type": "plane",
        "size": 5
    }
}


items2 = [
    {"name":"Foo","description":"There comes my hero"},
    {"name":"Red","description":"It's my aeroplane"}
]



@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


@app.get("/items2/", response_model=list[Item])
async  def read_items2():
    return  items2





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
