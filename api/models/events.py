from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class DeploymentEvent(BaseModel):
    repo_id: str
    event_type: str
    branch: str
    commit_sha: str
    payload: Dict
    received_at: datetime = datetime.utcnow()
