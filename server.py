from fastapi import FastAPI
import asyncio
import uvicorn
import os
import time


app = FastAPI()  ##Fast API App##
NAME = time.time()   ##Current Server Instance Name Initialisation(To identify which server got ping in last ##

PONG = ""  ## Temporary common global variable ##

@app.get("/ping")
def ping():
    global PONG, NAME
    if PONG == NAME:
        os.environ['PONG_LAST'] = NAME
        pong_time = os.getenv('PONG_TIME')
        print('Invoke other Server -Instance : /ping after PONG_TIME ms')
    return "pong"

async def init():         ## When Server Start it will initialize ##
    global PONG, NAME
    while True:
        pong_cmd = os.getenv('PONG_CMD')         ## Checked the env variable for start, pause, resume and stop ##
        if pong_cmd == 'start' or pong_cmd == 'resume':
            PONG = NAME
        elif pong_cmd == 'stop' or pong_cmd == 'pause':
            PONG = ""
        await asyncio.sleep(1)  ## Check every one second ##

@app.on_event("startup")
async def scheduler():
    loop = asyncio.get_event_loop()
    loop.create_task(init())



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8081)