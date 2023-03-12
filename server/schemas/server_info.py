from pydantic import BaseModel


class ServerInfoBase(BaseModel):
    id: int


# Properties to receive via API on creation
class ServerInfoCreate(BaseModel):
    host: str
    port: int
    cUsername: str
    cPassword: str
    database: str
    serverName: str = None
    verifyKey: str


# Properties to receive via API on update
class ServerInfoUpdate(ServerInfoCreate):
    id: int
