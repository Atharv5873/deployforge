from pymongo import MongoClient
from api.core.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

repos_collection = db.repositories
events_collection = db.deployment_events
builds_collection = db.builds
