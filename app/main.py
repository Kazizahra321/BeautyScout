from fastapi import FastAPI
from .router import embedding_router
from fastapi.middleware.cors import CORSMiddleware


# Create an instance of FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for development only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(embedding_router.router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World"}
