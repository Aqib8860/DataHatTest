# Data Hat Test

A weather and news app with authentication features.

## Features

- User Authentication with JWT access and refresh tokens
- Weather and News APIs integration with caching using Redis

## Installation

1. Clone the repo
   ```bash
   git clone https://github.com/yourusername/yourrepo.git

2. Navigate to the project directory
    cd yourrepo

3. Create a virtual environment and activate it
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

4. Install dependencies    
    pip install -r requirements.txt

Usage
Run the FastAPI server:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

## Environment Variables

Create a `.env` file in the root directory and add:

MONGODB_URL=your_mongodb_connection_string
DB_NAME=your_database_name
AUTH_SECRET_KEY=your_secret_key
AUTH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
NEWS_API_KEY=your_news_api_key
WEATHER_API_KEY=your_weather_api_key
REDIS_URL=redis://username:password@host:port/0


## API Endpoints

### 1. Signup
- URL: `http://127.0.0.1:8000/user/signup/`
- Method: `POST`
- Body:

```json
{
    "email": "test3@gmail.com",
    "password": "Test8860@",
    "full_name": "Aqib Khan"
}
```

- Response:
```json
{
    "_id": "6853ae65273b221c0f69aa40",
    "email": "test3@gmail.com",
    "password": "$2b$12$kWsYpztX9mB5uASfcgtD3OG/G3On5Zd9mP7dOo6Tzk4c5jxTFGRba",
    "full_name": "Aqib Khan",
    "status": "ACTIVE",
    "created_at": "2025-06-19T11:59:56.866000",
    "last_login": null
}
```

### 2. Login
- URL: `http://127.0.0.1:8000/user/login/`
- Method: `POST`
- Body:

```json
{
    "email": "test2@gmail.com",
    "password": "Test8860@"
}
```

- Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkBnbWFpbC5jb20iLCJpZCI6IjY4NTI2Y2E2MGU4MDJiMjVmNmRlZWJkMyIsImV4cCI6MTc1MDQxOTcyMH0.fFVo2wsvWQrUPM-_RRYLb5W7C-dU6mbLpg2Z-lzd_lk",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkBnbWFpbC5jb20iLCJpZCI6IjY4NTI2Y2E2MGU4MDJiMjVmNmRlZWJkMyIsImV4cCI6MTc1MDkzODEyMH0.jm5QYk79W4kS4Bceb9wwt96jY2FKUJsZT4fVB7awxAk",
    "token_type": "bearer",
    "user": {
        "_id": "68526ca60e802b25f6deebd3",
        "email": "test2@gmail.com",
        "full_name": "Aqib Khan",
        "status": "ACTIVE"
    }
}
```

### 3. Refresh Token
- URL: `http://127.0.0.1:8000/user/token/refresh/`
- Method: `POST`
- Body: 
```json
{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkBnbWFpbC5jb20iLCJpZCI6IjY4NTI2Y2E2MGU4MDJiMjVmNmRlZWJkMyIsImV4cCI6MTc1MDkzODEyMH0.jm5QYk79W4kS4Bceb9wwt96jY2FKUJsZT4fVB7awxAk"
}
```

- Response
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkBnbWFpbC5jb20iLCJpZCI6IjY4NTI2Y2E2MGU4MDJiMjVmNmRlZWJkMyIsImV4cCI6MTc1MDQyMDI2M30.sGhhNVvp-SQ5Tp4fdGPLr6_SjE2uc6KGAyNWXmSPMXU",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MkBnbWFpbC5jb20iLCJpZCI6IjY4NTI2Y2E2MGU4MDJiMjVmNmRlZWJkMyIsImV4cCI6MTc1MDkzODY2M30.ev5_-Ta-j3Axp5SQceMnUYwAjj7DddrGhFUqBcWXypY",
    "token_type": "bearer"
}
```

### 4. Get News
- URL: `http://127.0.0.1:8000/news?query=cricket&language=en&category=sports`
- Method: `GET`
- Authentication: Required (Pass access token in Authorization header)

- Response
```json
{
    "status": "success",
    "totalResults": 30146,
    "results": [
        {
            "article_id": "c7b4347f8ae854f1b25799185a0023fc",
            "title": "What to know about the impacts of the Supreme Court's ruling on transgender care for youth",
            "link": "https://ca.style.yahoo.com/know-impacts-supreme-courts-ruling-170054306.html",
            "keywords": [
                "news"
            ],
            "creator": [
                "The Canadian Press"
            ],
            "description": "The U.S. Supreme Court has upheld Tennessee's ban on gender-affirming surgery for transgender youth in a ruling that’s likely to reverberate across the country.",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-06-18 18:23:00",
            "pubDateTZ": "UTC",
            "image_url": "https://s.yimg.com/ny/api/res/1.2/I9ZnYOEri6REA4k4TrB5NQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD04MDA-/https://media.zenfs.com/en/cp_lifestyle_556/dae14b12f4bf5f41a10875e85e52e0e4",
            "video_url": null,
            "source_id": "yahoo",
            "source_name": "Yahoo! News",
            "source_priority": 17,
            "source_url": "https://news.yahoo.com",
            "source_icon": "https://n.bytvi.com/yahoo.png",
            "language": "english",
            "country": [
                "canada"
            ],
            "category": [
                "sports"
            ],
            "sentiment": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "sentiment_stats": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_tag": "ONLY AVAILABLE IN PROFESSIONAL AND CORPORATE PLANS",
            "ai_region": "ONLY AVAILABLE IN CORPORATE PLANS",
            "ai_org": "ONLY AVAILABLE IN CORPORATE PLANS",
            "duplicate": true
        },
    ]
}
```

### 5. Get Weather 
- URL: `http://127.0.0.1:8000/weather?state=Delhi&country=India`
- Method - `GET`

- Authentication: Not required
- Response
```json
{
"location": {
    "name": "Delhi",
    "region": "Delhi",
    "country": "India",
    "lat": 28.6667,
    "lon": 77.2167,
    "tz_id": "Asia/Kolkata",
    "localtime_epoch": 1750314319,
    "localtime": "2025-06-19 11:55"
},
"current": {
    "last_updated_epoch": 1750313700,
    "last_updated": "2025-06-19 11:45",
    "temp_c": 32.2,
    "temp_f": 90.0,
    "is_day": 1,
    "condition": {
        "text": "Mist",
        "icon": "//cdn.weatherapi.com/weather/64x64/day/143.png",
        "code": 1030
    },
    "wind_mph": 7.6,
    "wind_kph": 12.2,
    "wind_degree": 116,
    "wind_dir": "ESE",
    "pressure_mb": 998.0,
    "pressure_in": 29.47,
    "precip_mm": 0.0,
    "precip_in": 0.0,
    "humidity": 71,
    "cloud": 75,
    "feelslike_c": 36.6,
    "feelslike_f": 97.8,
    "windchill_c": 32.7,
    "windchill_f": 90.8,
    "heatindex_c": 37.6,
    "heatindex_f": 99.6,
    "dewpoint_c": 22.6,
    "dewpoint_f": 72.6,
    "vis_km": 2.8,
    "vis_miles": 1.0,
    "uv": 9.0,
    "gust_mph": 10.7,
    "gust_kph": 17.2
}
}
```
