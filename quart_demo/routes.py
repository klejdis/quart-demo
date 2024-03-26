import asyncio
from random import random
from typing import Any, Callable

from pydantic.main import BaseModel
from quart import Blueprint, request
from quart_schema import validate_request, validate_response
from sqlalchemy import Result, insert
from sqlalchemy.orm import selectinload
from werkzeug.exceptions import Unauthorized, BadRequest

from quart_demo.database.connection import async_session
from quart_demo.models.models import Comments, Posts
from quart_demo.services.base_dao import BaseDao

bp = Blueprint("", __name__)


def authenticated(func: Callable[..., Any]) -> Callable[..., Any]:
    async def decorator(*args: Any, **kwargs: Any) -> Any:
        if "Authorization" not in request.headers:
            raise Unauthorized
            # ToDo check the token against the token issuer
        return await func(*args, **kwargs)

    return decorator


class CreatedResponse(BaseModel):
    success: bool
    id: Any | None = None


class DeletedResponse(BaseModel):
    success: bool
    rowcount: int


@bp.route("/health")
async def hello() -> str:
    return "Hello, World!"


class PostsResponse(BaseModel):
    class Post(BaseModel):
        id: int
        name: str
        description: str

    posts: list[Post | None]


@bp.get("/posts")
@validate_response(PostsResponse)
@authenticated
async def posts() -> PostsResponse:
    rez = await BaseDao.get_all(Posts)
    return PostsResponse(posts=[{"id": row.id, "name": row.name, "description": row.description} for row in rez])


@bp.get("/posts/<int:post_id>")
async def post(post_id: int) -> dict[str, Any]:
    rez = await BaseDao.get_one(Posts, Posts.id == post_id)
    return {"id": rez.id, "name": rez.name, "description": rez.description}


class CreatePostRequest(BaseModel):
    name: str
    description: str


@bp.post("/posts")
@validate_request(CreatePostRequest)
async def create_post(data: CreatePostRequest) -> CreatedResponse:
    post = await BaseDao.create(Posts, **data.dict())
    return CreatedResponse(success=True, id=post.id)


class UpdatePostRequest(BaseModel):
    name: str | None
    description: str | None


@bp.put("/posts/<int:post_id>")
@validate_request(UpdatePostRequest)
async def update_post(post_id: int, data: UpdatePostRequest) -> dict[str, Any]:
    await BaseDao.update(Posts, Posts.id == post_id, **data.dict())
    return {"id": post_id, "name": data.name, "description": data.description}


@bp.delete("/posts/<int:post_id>")
async def delete_post(post_id: int) -> DeletedResponse:
    rowcount = await BaseDao.delete(Posts, Posts.id == post_id)
    return DeletedResponse(success=True, rowcount=rowcount)


class CommentsResponse(BaseModel):
    class Comment(BaseModel):
        id: int
        content: str

    comments: list[Comment | None]


@bp.get("/posts/<int:post_id>/comments")
async def comments(post_id: int) -> CommentsResponse:
    rez = await BaseDao.get_all(Comments, Comments.post_id == post_id, opt=selectinload(Comments.post))
    return CommentsResponse(comments=[{"id": row.id, "content": row.content} for row in rez])


class CreateCommentRequest(BaseModel):
    content: str


@bp.post("/posts/<int:post_id>/comments")
@validate_request(CreateCommentRequest)
async def create_comment(post_id: int, data: CreateCommentRequest) -> CreatedResponse:
    async with async_session.begin() as session:
        stmt = insert(Comments).values(post_id=post_id, content=data.content)
        result: Result[Any] = await session.execute(stmt)
    return CreatedResponse(success=True, id=result.lastrowid)  # type: ignore


@bp.delete("/comments/<int:comment_id>")
async def delete_comment(comment_id: int) -> DeletedResponse:
    rowcount = await BaseDao.delete(Comments, Comments.id == comment_id)
    return DeletedResponse(success=True, rowcount=rowcount)
