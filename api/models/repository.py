from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class RepositoryCreate(BaseModel):
    name: str
    git_url: HttpUrl
    branch: str = "main"
    dockerfile_path: str = "Dockerfile"

class RepositoryInDB(RepositoryCreate):
    id: Optional[str] = None
    created_at: datetime = datetime.utcnow()
