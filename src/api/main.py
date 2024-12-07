#TODO: delete this todo
from fastapi import FastAPI
from src.api.operations.router import router as operations_rt

app = FastAPI(title="Task API")

@app.get("/")
def read_root():
    return {"Message": "Hello, World!"}


app.include_router(operations_rt)
