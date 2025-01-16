from pydantic import BaseModel, Field

class UserDb(BaseModel):
    id: str = Field(alias="id")
    login: str
    password: str

