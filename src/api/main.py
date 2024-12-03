from fastapi import FastAPI

app = FastAPI(title="Task API")

@app.get("/")
def read_root():
    return {"Message": "Hello, World!"}



