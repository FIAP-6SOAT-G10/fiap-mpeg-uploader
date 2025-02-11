from fiap_mpeg_uploader.models.users.user_db import UserDb
from fiap_mpeg_uploader.infra.env.env import EnvManager
import boto3
import uuid
import traceback

async def pre_signed(user: UserDb, mime_type: str):
    try:
        bucket_name = "processor-in"
        folder_name = f"a_processar/{str(user.id)}"
        s3_client = create_s3_client()
        if not folder_name.endswith('/'):
            folder_name += '/'
        _uuid = str(uuid.uuid1())
        
        folder_name += f"{_uuid}"
        if mime_type == "video/mp4":
            folder_name += ".mp4"

        s3_client.put_object(Bucket=bucket_name, Key=folder_name)

        expiration=3600
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': folder_name, 'ContentType': mime_type},
            ExpiresIn=expiration,
        )
        return presigned_url, _uuid
    except Exception as e:
        traceback.print_exc()
        return None, None


def create_s3_client(region_name='us-east-1'):
    s3_client = boto3.client('s3', region_name=region_name)
    return s3_client
