from datetime import datetime,time,timedelta
from typing import Annotated
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Body

app =FastAPI ()


@app.put("/items/{item_id}")
async  def read_item(item_id:UUID,
                     start_datetime:Annotated[datetime,Body()],
                     end_datetime:Annotated[datetime,Body()],
                     process_after:Annotated[timedelta,Body()],
                     response_at:Annotated[time |None,Body()]= None,
                     ):
    start_process = start_datetime+process_after
    duration=end_datetime-start_process
    return {"item_id":item_id,"start_datetime":start_datetime,"end_datetime":end_datetime,"process_after":process_after,"response_at":response_at,"start_process":start_process,"duration":duration}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)