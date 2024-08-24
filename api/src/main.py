import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import fastapi_users
from auth.database import User, create_db_and_tables
from posts.database import Post, create_db_posts
from auth.manager import get_user_manager
from auth.shemas import UserCreate, UserRead
from posts.posts import router_post
from auth.auth import auth_backend





app = FastAPI()

app.include_router(router_post)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    await create_db_posts()


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/register",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )