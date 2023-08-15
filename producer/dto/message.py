from pydantic import BaseModel


class MessageData(BaseModel):
    accn_id: str  # noqa
    unsubscribe: bool
    msg_id: str


class ShorterUrlDto(BaseModel):
    url: str
    data: MessageData


class ShorterUrlCreate(BaseModel):
    msg_id: str
    original_url: str
    short_url: str
    data: MessageData

    class Config:
        from_attributes = True
