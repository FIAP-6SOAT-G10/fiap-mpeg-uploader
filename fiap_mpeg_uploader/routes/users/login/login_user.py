from fiap_mpeg_uploader.infra.db.mongo import MongoClient
from fiap_mpeg_uploader.models.users.user_dto import UserDTO
from fiap_mpeg_uploader.utils.hash import hash_text
from fiap_mpeg_uploader.infra.jwt.main import generate_jwt

async def login_user(user: UserDTO):
    try:
        hashed_password = hash_text(user.password)
        user_db = await MongoClient.build().read("users", {
            "login": user.login,
            "password": hashed_password
        })
        if not user_db:
            return
        token = generate_jwt({
            "id": str(user_db.get("_id"))
        }, "admin")
        return token
    except Exception as e:
        print(f"{e!s}")
