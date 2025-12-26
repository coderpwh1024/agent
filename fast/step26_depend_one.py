from http.client import HTTPException

import uvicorn
from fastapi import FastAPI

app = FastAPI()

data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {""}
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error:{e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
