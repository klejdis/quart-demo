from typing import Any

from pydantic.main import BaseModel
from quart import Blueprint
from quart_schema import validate_request
from sqlalchemy import insert

from quart_demo.database.connection import async_session
from quart_demo.models.models import Posts

bp = Blueprint("", __name__)


class CreatedResponse(BaseModel):
    success: bool
    id: Any | None = None


@bp.route("/hello")
async def hello() -> str:
    return "Hello, World!"


@bp.get("/posts")
async def posts() -> str:
    return "Posts"


@bp.get("/posts/<int:post_id>")
async def post(post_id: int) -> str:
    return f"Post {post_id}"


class CreatePostRequest(BaseModel):
    name: str
    description: str


@bp.post("/posts")
@validate_request(CreatePostRequest)
async def create_post(data: CreatePostRequest) -> CreatedResponse:
    async with async_session.begin() as session:
        stmt = insert(Posts).values(name=data.name, description=data.description)
        result = await session.execute(stmt)
    return CreatedResponse(success=True, id=result.lastrowid)


@bp.delete("/posts/<int:post_id>")
async def delete_post(post_id: int) -> str:
    return f"Post {post_id} deleted"
