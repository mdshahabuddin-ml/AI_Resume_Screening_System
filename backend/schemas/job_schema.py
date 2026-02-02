from pydantic import BaseModel
from typing import List

class JobRequest(BaseModel):
    title: str
    description: str
    skills: List[str]
