from fiap_mpeg_uploader.models.users.user_db import UserDb
import boto3

async def pre_signed(user: UserDb):
    try:
        bucket_name = ""
        folder_name = str(user.id)
        s3_client = create_s3_client()
        
        if not folder_name.endswith('/'):
            folder_name += '/'

        s3_client.put_object(Bucket=bucket_name, Key=folder_name)
    except Exception as e:
        print(f"{e!s}")


def create_s3_client(region_name='us-east-1'):
    s3_client = boto3.client('s3', region_name=region_name)
    return s3_client
