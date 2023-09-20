import logging

from pydantic import ValidationError
from quart import Quart, ResponseReturnValue
from quart_schema import Info, QuartSchema, RequestSchemaValidationError, ResponseSchemaValidationError, tag
from quart_schema.extension import security_scheme

from quart_demo.config import settings
from quart_demo.routes import bp

logger = logging.getLogger(__name__)


def create_app() -> Quart:
    app = Quart(__name__)
    app.config.from_object(settings.quart)
    app.register_blueprint(bp, url_prefix=f"{settings.base_path}")

    QuartSchema(
        app,
        info=Info(title="Quart Demo", version="0.0.1"),
        openapi_path=f"{settings.base_path}/openapi.json",
        swagger_ui_path=f"{settings.base_path}/docs",
        redoc_ui_path=f"{settings.base_path}/redocs",
        tags=[],
        security_schemes={"Bearer": {"type": "http", "scheme": "bearer"}},
        security=[{"Bearer": []}],
    )

    @app.errorhandler(RequestSchemaValidationError)  # type: ignore
    async def handle_request_validation_error(e: RequestSchemaValidationError) -> ResponseReturnValue:
        logger.info("Validation error for request", exc_info=e)
        if isinstance(e.validation_error, ValidationError):
            return {"error": e.validation_error.errors()}, 400
        else:
            return {"error": str(e.validation_error)}, 400

    @app.errorhandler(ResponseSchemaValidationError)  # type: ignore
    async def handle_response_validation_error(e: ResponseSchemaValidationError) -> ResponseReturnValue:
        logger.info("Validation error for response", exc_info=e)
        if isinstance(e.validation_error, ValidationError):
            return {"error": e.validation_error.errors()}, 500
        else:
            return {"error": str(e.validation_error)}, 500

    @tag(["Health Check"])
    @security_scheme([])
    @app.route("/health-check")
    async def health_check() -> ResponseReturnValue:
        return "Healthy as a horse!"

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8080)
