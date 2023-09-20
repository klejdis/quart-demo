from quart import Blueprint

bp = Blueprint("", __name__)


@bp.route("/hello")
def hello() -> str:
    return "Hello, World!"
