import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI();


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.post("/files2")
async def create_file2(file: bytes = File(description="A File read as bytes")):
    return {"file_size": len(file)}


@app.post("/uploadfile2")
async def create_upload_file2(file: UploadFile = File(description="A File read as UploadFile")):
    return {"filename": file.filename}


@app.post("/files3")
async  def create_files(files:list[bytes]=File()):
    print("多文件上传")
    return {"file_sizes": [len(file) for file in files]}



@app.post("/uploadfiles3")
async  def create_upload_files(files:list[UploadFile]):
    return {"filenames": [file.filename for file in files]}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
