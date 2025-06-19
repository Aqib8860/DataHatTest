from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from typing import Optional, Dict, Any


class MongoBaseModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Map _id to string

    @classmethod
    def from_mongo(cls, document: Dict[str, Any]):
        """ Convert MongoDB document (_id: ObjectId) to a serializable format """
        
        if document:
            if "_id" in document:
                document["_id"] = str(document["_id"])  # Convert ObjectId to string

        return cls(**document) if document else None

    @classmethod
    def get_collection(cls, db):
        """ Get the MongoDB collection name dynamically """
        return db[cls.Config.collection_name]  # Use Config for collection name


class UserProfileBase(MongoBaseModel):
    email: str | None = None
    password: str | None = None
    full_name: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    last_login: datetime | None = None


class UserProfileBaseList(MongoBaseModel):
    email: str | None = None
    full_name: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    last_login: datetime | None = None


class RegistrationBase(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    status: str | None = "ACTIVE"
    created_at: datetime | None = Field(default_factory=datetime.now)


class LoginBase(BaseModel):
    email: EmailStr
    password: str | None = None  


class TokenRefreshRequest(BaseModel):
    refresh_token: str
