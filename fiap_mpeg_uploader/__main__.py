from routes.users.main import users_router
from routes.pre_signed_url.main import pre_signed_router

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def health_check():
    return {"hello": "world"}

app.include_router(users_router, prefix="/api/v1")
app.include_router(pre_signed_router, prefix="/api/v1")

uvicorn.run(
    app,
    host="0.0.0.0",
    port=8080
)

