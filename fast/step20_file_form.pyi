import uvicorn
from fastapi import FastAPI, File, Form
from starlette.datastructures import UploadFile

app =FastAPI();


async  def create_file(file:bytes=File(),fileb:UploadFile=File(),token:str=Form()):
    return {
        "file_size":len(file),
        "token":token,
        "fileb_content_type":fileb.content_type,
    }



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)