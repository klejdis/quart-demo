import logging

from quart import Quart
from quart_schema import Info, QuartSchema

from quart_demo.config import settings
from quart_demo.routes import bp

logger = logging.getLogger(__name__)


def create_app() -> Quart:
    app = Quart(__name__)
    # load the settings from the config file
    app.config.from_object(settings.quart)
    # this will prefix all routes with the base path
    app.register_blueprint(bp, url_prefix=f"{settings.base_path}")

    QuartSchema(
        app,
        info=Info(title="Quart Demo", version="0.0.1"),
        openapi_path=f"{settings.base_path}/openapi.json",
        swagger_ui_path=f"{settings.base_path}/docs",
        redoc_ui_path=f"{settings.base_path}/redocs",
        tags=[],
        # security_schemes={"Bearer": {"type": "http", "scheme": "bearer"}}, # TODO: add security scheme
        security=[{"Bearer": []}],
    )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8085)
