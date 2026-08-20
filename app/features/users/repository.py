"""MongoDB persistence queries owned by the user-management feature."""

from typing import Any

from bson import ObjectId
from pymongo.collection import Collection


class UserRepository:
    """Persistence boundary for the shared `users` collection."""

    def __init__(self, collection: Collection):
        self._collection = collection

    def find_by_email(self, email: str) -> dict[str, Any] | None:
        document = self._collection.find_one({"email": email})
        return self._serialize(document) if document else None

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        document = self._collection.find_one({"username": username})
        return self._serialize(document) if document else None

    def create(self, document: dict[str, Any]) -> dict[str, Any]:
        result = self._collection.insert_one(document)
        document["_id"] = result.inserted_id
        return self._serialize(document)

    @staticmethod
    def _serialize(document: dict[str, Any]) -> dict[str, Any]:
        serialized = document.copy()
        serialized["id"] = str(serialized.pop("_id"))
        for field in ("college_id", "library_id"):
            if isinstance(serialized.get(field), ObjectId):
                serialized[field] = str(serialized[field])
        for field in ("created_at", "updated_at"):
            if field in serialized:
                serialized[field] = serialized[field].isoformat()
        return serialized
