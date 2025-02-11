from pydantic import BaseModel, field_validator, Field, AliasChoices
from typing import Any
from pydantic_mongo import ObjectIdField

class UserDb(BaseModel):
    id: str | ObjectIdField = Field(alias="id", validation_alias=AliasChoices("id", "_id"))
    login: str
    password: str
    name: str
    email: str

    @field_validator("id")
    @classmethod
    def convert_object_id_into_str(cls, data: Any) -> Any:  
        if isinstance(data, ObjectIdField):  
            return str(data)
        return data
