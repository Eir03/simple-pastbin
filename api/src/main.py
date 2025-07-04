import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.database import init_roles
from database import init_db
from posts.database import init_categories
from database import get_async_session
from posts.posts import router_post
from auth.auth import router_auth

app = FastAPI()

app.include_router(router_post)
app.include_router(router_auth)

@app.on_event("startup")
async def on_startup():
    # Инициализация общей структуры БД
    await init_db()
    
    # Инициализация данных
    async for session in get_async_session():
        # Инициализация ролей пользователей
        await init_roles(session)
        # Инициализация категорий для постов
        await init_categories(session)
        print("База данных успешно инициализирована")


# fastapi_users = fastapi_users.FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )

# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth/register",
#     tags=["auth"],
# )

# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)