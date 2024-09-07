from fastapi import FastAPI
from .router import embedding_router

# Create an instance of FastAPI
app = FastAPI()

app.include_router(embedding_router.router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World"}
