from pydantic import BaseModel


class RolesBase(BaseModel):
    id: int


# Properties to receive via API on creation
class RolesCreate(BaseModel):
    roleId: int
    roleName: str


# Properties to receive via API on update
class RolesUpdate(RolesCreate):
    ...
