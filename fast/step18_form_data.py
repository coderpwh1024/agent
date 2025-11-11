import uvicorn
from fastapi import FastAPI, Form

app = FastAPI ()


@app.post("/login")
async  def login(username:str=Form(),password:str=Form()):
    return {"username":username,"password":password}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)