import uvicorn
from fastapi import FastAPI, File

app = FastAPI();



@app.post("/files/")
async  def create_upload_file(file:bytes=File()):
    return {"file_size":len(file)}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
