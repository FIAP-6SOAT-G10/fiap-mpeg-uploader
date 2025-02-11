import traceback
import json
import boto3
from typing import Any
from bson import ObjectId
from fiap_mpeg_uploader.routes.pre_signed_url.models.process_protocol_model import ProcessProtocolRequest
from fiap_mpeg_uploader.infra.env.env import EnvManager
from fastapi.responses import JSONResponse
from fiap_mpeg_uploader.infra.db.mongo import MongoClient
from fiap_mpeg_uploader.models.users.user_db import UserDb

async def process_protocol(req: ProcessProtocolRequest):
    try:
        env_manager: EnvManager = EnvManager()
        queue_url = env_manager.get("QUEUE_URL")
        sqs = boto3.client('sqs', region_name='us-east-1')
        user_db: dict[Any, Any] | None = await MongoClient.build().read("users", {
            "_id": ObjectId(req.userId),
        })
        if not user_db:
            raise Exception(f"User {req.userId} not found!")
        user: UserDb = UserDb(**user_db)

        body = json.dumps({
            "protocol": req.protocolId,
            "user": {
                "name": user.name,
                "email": user.email
            }
        })

        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=body
        )
        if not response:
            raise Exception(f"Trying to upload message and failed: {body}")
        return JSONResponse(status_code=500, content={
            "msg": response
        }) 
    except Exception as e:
        traceback.print_exc()
        msg = str(e)
        return JSONResponse(status_code=500, content={
            "debug": msg
        }) 