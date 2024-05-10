from dotenv import load_dotenv
from fastapi import FastAPI
import logging
from endpoints.v0 import router as v0_router
from endpoints.v1 import router as v1_router
from endpoints.v2 import router as v2_router

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.include_router(v0_router, prefix="/v0")
app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")

@app.get("/")
async def read_root():
    return {"message": "Hello from the backend"}
