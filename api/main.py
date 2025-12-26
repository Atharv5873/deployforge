from fastapi import FastAPI
from api.routers import repos
from api.routers import webhooks




app = FastAPI(
    title="DeployForge",
    description="GitOps-style deployment automation platform",
    version="0.1.0",
)

app.include_router(repos.router)
app.include_router(webhooks.router)

@app.get("/")
def root():
    return {"status": "DeployForge API running"}
