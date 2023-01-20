from fastapi import FastAPI
from database import Base, engine
from routers import registration, users, contents, authentication, likes, playlists, subscriptions, feed, profile, \
    comments
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(registration.router)
app.include_router(users.router)
app.include_router(contents.router)
app.include_router(authentication.router)
app.include_router(likes.router)
app.include_router(playlists.router)
app.include_router(subscriptions.router)
app.include_router(feed.router)
app.include_router(profile.router)
app.include_router(comments.router)

Base.metadata.create_all(engine)
