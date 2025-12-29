from fastapi import APIRouter, Request, HTTPException
from api.services.webhook_security import verify_github_signature
from api.services.mongo import repos_collection, events_collection
import os

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

@router.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()

    repo_url = payload["repository"]["html_url"].rstrip(".git")
    branch = payload["ref"].split("/")[-1]
    commit_sha = payload["after"]   # ✅ THIS WAS MISSING

    if branch != "main":
        return {"message": "Ignored non-main branch push"}

    repo = repos_collection.find_one({"git_url": repo_url})
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not registered")

    existing = events_collection.find_one({
        "repo_id": repo["_id"],
        "commit_sha": commit_sha
    })

    if existing:
        return {"message": "Deployment event already registered"}

    event = {
        "repo_id": repo["_id"],
        "event_type": "push",
        "branch": branch,
        "commit_sha": commit_sha,
        "payload": payload
    }

    events_collection.insert_one(event)
    return {"message": "Deployment event registered"}
    
