from fastapi import FastAPI

app = FastAPI(
    title="DeployForge",
    description="GitOps-style deployment automation platform",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"status": "DeployForge API running"}
