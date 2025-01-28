from pydantic import BaseModel, Field

class UserDTO(BaseModel):
    login: str
    password: str
    name: str | None = Field(None)
    email: str | None = Field(None)
