FROM europe-west3-docker.pkg.dev/y42-artifacts-ea47981a/main/y42-python-3.10-build:dev AS build
COPY pyproject.toml poetry.lock ./
ARG INSTALL_DEV_DEPS
RUN --mount=type=ssh  \
    if [ -z "$INSTALL_DEV_DEPS" ] ; then poetry install --only main --no-interaction ; else poetry install --no-interaction ; fi

FROM europe-west3-docker.pkg.dev/y42-artifacts-ea47981a/main/y42-python-3.10-base:dev

ARG SHORT_SHA
ENV DD_VERSION=${SHORT_SHA}
ENV OTEL_RESOURCE_ATTRIBUTES=service.version=${DD_VERSION}

COPY --from=build /app/.venv /app/.venv
COPY . .
ENV PYTHONPATH=.
ENV PATH="/app/.venv/bin:$PATH"

USER klejdis

CMD ["hypercorn", "--config=hypercorn.toml", "quart_demo/asgi:app"]
