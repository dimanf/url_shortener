from pydantic import BaseModel


class VisitedUrlCreateDto(BaseModel):
    short_url: str
    accn_id: str  # noqa
    unsubscribe: bool

    class Config:
        from_attributes = True
