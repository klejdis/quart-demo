from typing import Any

from pydantic.main import BaseModel
from quart import Blueprint
from quart_schema import validate_request, validate_response
from sqlalchemy import Result, delete, insert, select

from quart_demo.database.connection import async_session
from quart_demo.models.models import Posts

bp = Blueprint("", __name__)


class CreatedResponse(BaseModel):
    success: bool
    id: Any | None = None


class DeletedResponse(BaseModel):
    success: bool
    rowcount: int


@bp.route("/hello")
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
async def posts() -> PostsResponse:
    async with async_session.begin() as session:
        result = await session.execute(select(Posts))
        rez = result.scalars().all()
        return PostsResponse(posts=[{"id": row.id, "name": row.name, "description": row.description} for row in rez])


@bp.get("/posts/<int:post_id>")
async def post(post_id: int) -> dict[str, Any]:
    async with async_session.begin() as session:
        result = await session.execute(select(Posts).where(Posts.id == post_id))
        rez = result.scalars().first()
        return {"id": rez.id, "name": rez.name, "description": rez.description}


class CreatePostRequest(BaseModel):
    name: str
    description: str


@bp.post("/posts")
@validate_request(CreatePostRequest)
async def create_post(data: CreatePostRequest) -> CreatedResponse:
    async with async_session.begin() as session:
        stmt = insert(Posts).values(name=data.name, description=data.description)
        result: Result[Any] = await session.execute(stmt)
    return CreatedResponse(success=True, id=result.lastrowid)  # type: ignore


@bp.delete("/posts/<int:post_id>")
async def delete_post(post_id: int) -> DeletedResponse:
    async with async_session.begin() as session:
        stmt = delete(Posts).where(Posts.id == post_id)
        result = await session.execute(stmt)

    return DeletedResponse(success=True, rowcount=result.rowcount)
