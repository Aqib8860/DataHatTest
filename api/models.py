from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Literal
from fastapi import UploadFile


class MongoBaseModel(BaseModel):
    """
    Base model for MongoDB documents to handle ObjectId conversion.
    """
    id: Optional[str] = Field(default=None, alias="_id")  # Map _id to string

    @classmethod
    def from_mongo(cls, document: Dict[str, Any]):
        """ Convert MongoDB document (_id: ObjectId) to a serializable format """
        
        if document:
            if "_id" in document:
                document["_id"] = str(document["_id"])  # Convert ObjectId to string

            # if "created_at" in document:
            #     document["created_at"] = str(document["created_at"])  # Convert created_at to string

            # if "updated_at" in document:
            #     document["created_at"] = str(document["created_at"])  # Convert updated_at to string

        return cls(**document) if document else None

    @classmethod
    def get_collection(cls, db):
        """ Get the MongoDB collection name dynamically """
        return db[cls.Config.collection_name]  # Use Config for collection name


class UserProfile(MongoBaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


    class Config:
        collection_name = "users"


