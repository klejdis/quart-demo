from pydantic.main import BaseModel
from quart import Blueprint

bp = Blueprint("", __name__)


@bp.route("/hello")
def hello() -> str:
    return "Hello, World!"


@bp.route("/posts")
def posts() -> str:
    return "Posts"


@bp.route("/posts/<int:post_id>")
def post(post_id: int) -> str:
    return f"Post {post_id}"
