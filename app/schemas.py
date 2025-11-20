from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ItemBase(BaseModel):
    title: constr(min_length=1, max_length=200)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemOut(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
