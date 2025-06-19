from fastapi import APIRouter, Depends, Request

from slowapi.util import get_remote_address
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .schemas import RegistrationBase, UserProfileBase, LoginBase, UserProfileBaseList, TokenRefreshRequest

from .auth import hash_password, get_current_user
from . import views
from database import get_database  # Import the correct dependency


limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


# ---------------------- Authentication ----------------------------------------------------

# User Registrations
@router.post("/user/signup/", response_model=UserProfileBase)
async def user_registration(
    userprofile:RegistrationBase, db=Depends(get_database)
):
    # Hash password before saving
    userprofile.password = hash_password(userprofile.password)
    return await views.user_registartion_view(db=db, userprofile=userprofile)


# User Login
@router.post("/user/login/")
async def user_login(
    request: Request,
    user_login: LoginBase, db=Depends(get_database)
):
    return await views.user_login_view(db, request, user_login)


# Refresh Token
@router.post("/user/token/refresh/")
async def refresh_token(
    data: TokenRefreshRequest 
):
    return await views.refresh_token_view(data=data)


# Get User Profiles
@router.get("/userprofiles/", response_model=list[UserProfileBaseList])
async def get_user_profiles(    
    db=Depends(get_database)):
    return await views.get_user_profiles_view(db)

# ========================================================================================================================


# Get News
@router.get("/news")
@limiter.limit("5/minute")
async def get_news(
    request: Request,
    search: str | None = None,
    language: str | None = None,
    category: str | None = None,
    db=Depends(get_database),
    user: dict = Depends(get_current_user)
):
    return await views.get_news_view(db=db, search=search, language=language, category=category)


# Get Weather
@router.get("/weather")
@limiter.limit("5/minute")
async def get_weather(
    request: Request,
    state: str,
    country: str
):
    return await views.get_weather_view(state=state, country=country)

