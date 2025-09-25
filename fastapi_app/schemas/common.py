from pydantic import BaseModel

class ListParams(BaseModel):
    limit: int = 20
    offset: int = 0
    q: str | None = None
