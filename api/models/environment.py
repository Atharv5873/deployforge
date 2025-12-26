from pydantic import BaseModel
from typing import Dict

class Environment(BaseModel):
    name: str
    variables: Dict[str,str]
