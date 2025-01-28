from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fiap_mpeg_uploader.models.users.user_dto import UserDTO
from fiap_mpeg_uploader.routes.users.create.create_users import create_user

from fiap_mpeg_uploader.routes.users.login.login_user import login_user

users_router = APIRouter()

@users_router.post("/users")
async def create_users(user: UserDTO):
    try:
        if not user.email:
            return JSONResponse(status_code=400, content={"status": "E-mail not found"})
        if not user.name:
            return JSONResponse(status_code=400, content={"status": "Name must be provided"})
        ok = await create_user(user)
        if ok:
            return JSONResponse(status_code=201, content={"status": f"created {ok.inserted_id!s}"})
        return JSONResponse(status_code=400, content={"status": "not created"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": f"Error: {e!s}"})

@users_router.post("/login")
async def login(user: UserDTO):
    try:
        token = await login_user(user)
        if not token:
            return JSONResponse(status_code=400, content={"status": "user not found"})
        return JSONResponse(status_code=200, content={"token": token}) 
    except Exception as e:
        print(f"{e!s}")    
