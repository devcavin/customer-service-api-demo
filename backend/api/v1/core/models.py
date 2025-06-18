from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotesNew(BaseModel):
    title: str
    content: str


class NotesDetails(NotesNew):
    id: int
    created_at: datetime

class NotesUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

