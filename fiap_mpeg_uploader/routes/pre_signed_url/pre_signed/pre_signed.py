from fiap_mpeg_uploader.models.users.user_db import UserDb
import boto3
import uuid

async def pre_signed(user: UserDb, mime_type: str):
    try:
        bucket_name = "fiap-hackathon"
        folder_name = str(user.id)
        s3_client = create_s3_client()
        
        if not folder_name.endswith('/'):
            folder_name += '/'
        _uuid = str(uuid.uuid1())
        print(_uuid)
        folder_name += f"{_uuid}"
        s3_client.put_object(Bucket=bucket_name, Key=folder_name)

        expiration=3600
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': folder_name, 'ContentType': mime_type},
            ExpiresIn=expiration,
        )
        return presigned_url
    except Exception as e:
        print(f"{e!s}")


def create_s3_client(region_name='us-east-1'):
    s3_client = boto3.client('s3', region_name=region_name)
    return s3_client
