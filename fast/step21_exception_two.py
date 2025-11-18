import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}))





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
