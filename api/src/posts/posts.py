from datetime import datetime, timezone
from hash_gen.hash_gen import get_hash
from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import URL_BLOB, BUCKET, USE_BLOB
from posts.blob import upload_text_to_s3
from posts.database import Post, get_async_session
from posts.models import PostCreate, PostRead

router_post = APIRouter(
    prefix='/posts',
    tags=['posts']
)

# async def get_hash_from_service():
#     async with httpx.AsyncClient() as client:
#         response = await client.get(URL_HASH_GEN + "/get-hash")
#         if response.status_code != 200:
#             raise HTTPException(status_code=500, detail="Failed to generate hash")
#         return response.json().get("hash")

@router_post.get('')
async def get_posts():
    return ''

@router_post.post('', response_model=PostRead)
async def create_post(post: PostCreate, session: AsyncSession = Depends(get_async_session)):
    hash_value = await get_hash()

    if USE_BLOB:
        content_post = None
        blob_storage_url = upload_text_to_s3(BUCKET, f'{hash_value}', post.content)

        if blob_storage_url is None:
            raise HTTPException(status_code=500, detail="Failed to upload content to S3")
    else:
        blob_storage_url = 'None'
        content_post = post.content
    
    now = datetime.now(timezone.utc)

    new_post = Post(
        title=post.title,
        hash=hash_value,
        blob_storage_url=blob_storage_url,
        category_id=post.category_id,
        is_public=post.is_public,
        created_at=now,
        delete_after_reading=post.delete_after_reading,
        tags=post.tags,
        expires_at=post.expires_at,
        content=content_post
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return PostRead.model_validate(new_post)

@router_post.get('/{hash_id}', response_model=PostRead)
async def get_post(hash_id: str, session: AsyncSession = Depends(get_async_session)):
    # Добавить удаление после прочтения
    # Добавить приватность

    result = await session.execute(select(Post).where(Post.hash == hash_id))
    result = result.scalars().first()
    if result is None:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return PostRead.model_validate(result)
    

@router_post.put('/{hash_id}')
async def update_post(hash_id: str, session: AsyncSession = Depends(get_async_session)):
    return None

# Нужно добавить что удалить может только сам пользователь
@router_post.delete('/{hash_id}')
async def delete_post(hash_id: str):
    return None

# Посты должны иметь публичный доступ
@router_post.get('/get_by_user/{user_id}')
async def get_by_user(user_id: str):
    return None
