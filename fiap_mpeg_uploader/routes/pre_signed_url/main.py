from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fiap_mpeg_uploader.models.users.user_db import UserDb
from fiap_mpeg_uploader.infra.db.mongo import MongoClient
from fiap_mpeg_uploader.routes.pre_signed_url.pre_signed.pre_signed import pre_signed
from fiap_mpeg_uploader.routes.pre_signed_url.pre_signed.process_protocol import process_protocol
from fiap_mpeg_uploader.infra.jwt.main import decode_jwt
from bson import ObjectId
from fiap_mpeg_uploader.routes.pre_signed_url.models.process_protocol_model import ProcessProtocolRequest
import traceback
from pydantic import BaseModel
from typing import Any


pre_signed_router = APIRouter()

@pre_signed_router.get("/pre-signed-s3")
async def login(request: Request, mime_type: str):
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
        url_pre_signed, protocol_id = await pre_signed(user, mime_type)
        if not url_pre_signed:
            return JSONResponse(status_code=401, content={"message": "URL unable to generate!"})
        
        return JSONResponse(status_code=200, content={
            "success": True, 
            "url": url_pre_signed,
            "protocolId": protocol_id
        }) 
    except Exception as e:
        traceback.print_exc()
        print(f"{e!s}")  

@pre_signed_router.post("/process")
async def process(req: ProcessProtocolRequest):
    try:
        await process_protocol(req)
    except Exception as e:
        traceback.print_exc()
        msg = str(e)
        return JSONResponse(status_code=500, content={
            "debug": msg
        }) 
