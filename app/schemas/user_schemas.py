from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    id: int
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    password: str