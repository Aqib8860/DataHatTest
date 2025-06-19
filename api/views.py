import os
import jwt
import requests
from fastapi import Depends, HTTPException
from fastapi_cache.decorator import cache
from datetime import datetime
from .models import UserProfile
from .schemas import UserProfileBase, TokenRefreshRequest

from .auth import verify_password, create_access_token, create_refresh_token, decode_refresh_token

from bson import ObjectId
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()


async def user_registartion_view(db: Depends, userprofile: dict):
    userprofile_collection = UserProfile.get_collection(db)

    userprofile = userprofile.model_dump()

    exists = await userprofile_collection.find_one({"email": userprofile["email"]})
    if exists:
        return JSONResponse({"error": "Profile already exists"}, status_code=400)
    
    created_profile = await userprofile_collection.insert_one(userprofile)
    userprofile = await userprofile_collection.find_one({"_id": created_profile.inserted_id})

    return UserProfileBase.from_mongo(userprofile)


async def user_login_view(db, request, user_login):
    try:
        userprofile_collection = UserProfile.get_collection(db)        
        
        # Find the user by email
        user = await userprofile_collection.find_one({"email": user_login.email})

        if user is None or not verify_password(user_login.password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Generate JWT token
        access_token = create_access_token(data={"sub": user["email"], "id": str(user["_id"])})
        refresh_token = create_refresh_token(data={"sub": user["email"], "id": str(user["_id"])})

        # Update last_login timestamp
        await userprofile_collection.update_one(
            {"_id": ObjectId(user["_id"])},  
            {"$set": {"last_login": datetime.now()}}
        )

        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer", 
            "user": {
                "_id": str(user["_id"]), "email": user["email"], "full_name": user["full_name"], "status": user["status"], 
            },
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# =================================================================================================

async def refresh_token_view(data: TokenRefreshRequest):
    try:
        # Decode refresh token

        payload = decode_refresh_token(data)

        # Generate new access and refresh tokens
        access_token = create_access_token({"sub": payload["sub"], "id": payload["id"]})
        refresh_token = create_refresh_token({"sub": payload["sub"], "id": payload["id"]})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    


async def get_user_profiles_view(db):
    userprofiles = await UserProfile.get_collection(db).find({}).to_list(length=None)

    if userprofiles:
        return userprofiles
    return JSONResponse([])


@cache(expire=60)
async def get_news_view(db: Depends, search: str, language: str, category: str):
    try:
        news_api_key = os.environ.get("NEWS_API_KEY")
        
        url = f"https://newsdata.io/api/1/latest?apikey={news_api_key}"
        params = {}

        if search:
            params["q"] = search
        if language:
            params["language"] = language
        if category:
            params["category"] = category

        headers = {"accept": "application/json"}
        
        response = requests.get(url=url, params=params, headers=headers, timeout=60) 
        return response.json()
            
        # return JSONResponse(response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@cache(expire=60)
async def get_weather_view(state: str, country: str):
    try:
        weather_api_key = os.environ.get("WEATHER_API_KEY")
        
        if not state or not country:
           raise HTTPException(status_code=400, detail="State and country required")
        
        url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={state},{country}"
        
        headers = {"accept": "application/json"}
           
        response = requests.get(url=url, headers=headers, timeout=60) 
        
        # return JSONResponse(response.json(), status_code=response.status_code)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
