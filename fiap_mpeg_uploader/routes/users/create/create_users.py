from fiap_mpeg_uploader.models.users.user_dto import UserDTO

from fiap_mpeg_uploader.infra.db.mongo import MongoClient
from fiap_mpeg_uploader.utils.hash import hash_text

async def create_user(user: UserDTO):
    try:
        new_password = hash_text(user.password)
        user.password = new_password
        mongo_client = MongoClient.build()
        inserted = await mongo_client.create("users", user.model_dump())
        if inserted:
            return inserted
    except Exception as e:
        print(f"{e!s}")

