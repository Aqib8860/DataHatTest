import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from database import lifespan
from api.urls import router
from logging_config import setup_logging


setup_logging()

# Initialize FastAPI with database lifespan
app = FastAPI(lifespan=lifespan)

allowed_origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # max_age=600 # for cache
)

allowed_host = ["localhost", "127.0.0.1"]

app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_host)


# Include the router
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
