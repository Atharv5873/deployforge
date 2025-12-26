from fastapi import APIRouter, Request, HTTPException
from api.services.webhook_security import verify_github_signature
from api.services.mongo import repos_collection, events_collection
import os

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

@router.post("/github")
async def github_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_github_signature(GITHUB_SECRET, body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()

    if payload.get("ref", "").endswith("/main") is False:
        return {"message": "Ignored non-main branch push"}

    git_url = payload["repository"]["html_url"]

    repo = repos_collection.find_one({"git_url": git_url})
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not registered")

    event = {
        "repo_id": str(repo["_id"]),
        "event_type": "push",
        "branch": "main",
        "commit_sha": payload["after"],
        "payload": payload,
    }

    events_collection.insert_one(event)

    # Phase 3 will enqueue jobs here
    return {"message": "Deployment event registered"}
