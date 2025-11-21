import uvicorn
from fastapi import FastAPI,HTTPException
from fastapi.exception_handlers import(
    http_exception_handler,
request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI();


@app.exception_handler(StarletteHTTPException)
async  def custom_http_exception_handler(request,exc):
    print(f"OMG! http 请求错误:{repr(exc)}")
    return  await custom_http_exception_handler(request,exc)







if __name__ =="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
