from fastapi import APIRouter, HTTPException
from api.models.repository import RepositoryCreate
from api.services.mongo import repos_collection
from bson import ObjectId
from api.services.git import validate_repo

router = APIRouter(prefix="/repos", tags=["Repositories"])

@router.post("")
def register_repo(repo: RepositoryCreate):
    if repos_collection.find_one({"git_url": str(repo.git_url)}):
        raise HTTPException(status_code=400, detail="Repository already registered")

    try:
        validate_repo(str(repo.git_url), repo.branch)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Git validation failed: {e}")

    repo_doc = repo.dict()
    repo_doc["git_url"] = str(repo.git_url)
    
    repos_collection.insert_one(repo_doc)
    return {"message": "Repository registered successfully"}

@router.get("")
def list_repos():
    repos = []
    for r in repos_collection.find():
        r["_id"] = str(r["_id"])
        repos.append(r)
    return repos

@router.get("/{repo_id}")
def get_repo(repo_id: str):
    repo = repos_collection.find_one({"_id": ObjectId(repo_id)})
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    repo["_id"] = str(repo["_id"])
    return repo
