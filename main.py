from typing import Union
from fastapi import FastAPI
from myKafka.consumer import TestConsumer, Consumer, SummaryConsumer, WorkbookConsumer
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()
c1 = SummaryConsumer()
c2 = WorkbookConsumer()
WORKERS = 6

@app.get("/")
def read_root(): return {"Hello": "World"}

@app.get('/test')
def test(): return "Test Response"

@app.on_event("startup")
async def startup_event():
    with ThreadPoolExecutor(WORKERS) as executor:
        executor.submit(start, c1)
        executor.submit(start, c2)
    
@app.on_event("shutdown")
def shutdown_event():
    with ThreadPoolExecutor(WORKERS) as executor:
        executor.submit(stop, c1)
        executor.submit(stop, c2)

def start(consumer: Consumer): consumer.run()
def stop(consumer: Consumer): consumer.close()
