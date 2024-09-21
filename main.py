from fastapi import FastAPI
from myKafka.consumer import Consumer, SummaryConsumer, WorkbookConsumer
import asyncio

app = FastAPI()

# Kafka Consumers
c1 = SummaryConsumer()
c2 = WorkbookConsumer()
consumer_tasks = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/test')
def test():
    return "Test Response"

async def start_consumer(consumer: Consumer):
    try:
        await asyncio.to_thread(consumer.run)
    except Exception as e:
        print(f"Error starting consumer: {consumer}, {e}")

async def stop_consumer(consumer: Consumer):
    try:
        await asyncio.to_thread(consumer.close)
    except Exception as e:
        print(f"Error stopping consumer: {consumer}, {e}")

@app.on_event("startup")
async def startup_event():
    global consumer_tasks
    consumer_tasks = [
        asyncio.create_task(start_consumer(c1)),
        asyncio.create_task(start_consumer(c2)),
    ]
    print("Consumers started.")

@app.on_event("shutdown")
async def shutdown_event():
    for task in consumer_tasks: task.cancel()
    await asyncio.gather(
        stop_consumer(c1),
        stop_consumer(c2),
        return_exceptions=True
    )
    print("Consumers stopped.")
