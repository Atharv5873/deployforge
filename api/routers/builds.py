from fastapi import APIRouter, HTTPException
from api.services.mongo import repos_collection, builds_collection, db
from api.services.builder import build_image
from bson import ObjectId

router = APIRouter(prefix="/builds", tags=["Builds"])

@router.post("/{event_id}")
def trigger_build(event_id: str):
    event = db.deployment_events.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    repo = repos_collection.find_one({"_id": event["repo_id"]})
    image_tag = f"{repo['name']}:{event['commit_sha'][:7]}"

    code, logs = build_image(repo["git_url"], event["commit_sha"], image_tag)

    build_doc = {
        "repo_id": str(event["repo_id"]),   
        "commit_sha": event["commit_sha"],
        "image_tag": image_tag,
        "status": "success" if code == 0 else "failed",
        "logs": logs
    }
    

    result = builds_collection.insert_one(build_doc)
    
    build_doc["_id"] = str(result.inserted_id)
    return build_doc
    
