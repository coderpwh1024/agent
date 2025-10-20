from fastapi import  FastAPI

app = FastAPI()


@app.get("/")
async def root():
    print("这是FastAPI")
    return {"message": "Hello World"}