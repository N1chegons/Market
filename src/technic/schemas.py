from datetime import datetime

from fastapi import Query
from pydantic import BaseModel

class Procreate(BaseModel):
    title: str | None = Query(max_length=100)
    description: str
    price: int
    cat_id: int | None = Query(ge=1, lt=5)
    created_at: datetime
