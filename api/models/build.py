from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Build(BaseModel):
    repo_id: str
    commit_sha: str
    image_tag: str
    status: str  # pending | success | failed
    logs: Optional[str] = None
    created_at: datetime = datetime.utcnow()
