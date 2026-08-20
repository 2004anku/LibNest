"""MongoDB client setup shared by feature repositories."""

from functools import lru_cache

from pymongo import MongoClient

from app.core.config import settings


@lru_cache
def get_mongo_client() -> MongoClient:
    """Create a single process-wide MongoDB client."""
    return MongoClient(settings.mongodb_uri)


def get_database():
    """Return the shared LibNest database; connection setup remains lazy."""
    return get_mongo_client()[settings.mongodb_database]
