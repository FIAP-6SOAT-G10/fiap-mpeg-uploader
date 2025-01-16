from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fiap_mpeg_uploader.models.users.user_db import UserDb
from fiap_mpeg_uploader.infra.db.mongo import MongoClient
from fiap_mpeg_uploader.routes.pre_signed_url.pre_signed.pre_signed import pre_signed
from fiap_mpeg_uploader.infra.jwt.main import decode_jwt
from bson import ObjectId
from typing import Any


pre_signed_router = APIRouter()

@pre_signed_router.get("/pre-signed-s3")
async def login(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"message": "Invalid or missing Bearer token"})
        auth_header = auth_header.replace("Bearer ", "")
        token = decode_jwt(auth_header, "admin")
        if not token or not token.get("id", None):
            return JSONResponse(status_code=401, content={"message": "Invalid or missing Bearer token"})
        
        user_db: dict[Any, Any] | None = await MongoClient.build().read("users", {
            "_id": ObjectId(token.get("id")),
        })

        if not user_db:
            return JSONResponse(status_code=401, content={"message": "User not found!"})

        user_db['id'] = str(user_db['_id'])

        user: UserDb = UserDb(**user_db)
        await pre_signed(user)
        # pre_signed()
        return JSONResponse(status_code=200, content={"success": True}) 
    except Exception as e:
        print(f"{e!s}")        
