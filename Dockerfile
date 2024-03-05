FROM python:3.10-slim

# update all depedencies
ENV DEFAULT_PACKAGES="curl git openssh-client build-essential"
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends --no-upgrade $DEFAULT_PACKAGES && \
    rm -rf /var/lib/apt/lists/*


# create working directory
WORKDIR /app

# setup poetry
RUN pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

# setup github with ssh
RUN mkdir -p -m 0600 ~/.ssh && \
    ssh-keyscan -H github.com > ~/.ssh/known_hosts && \
    git config --global url."git@github.com:".insteadOf "https://github.com/"

COPY pyproject.toml poetry.lock ./
ARG INSTALL_DEV_DEPS
RUN --mount=type=ssh  \
    if [ -z "$INSTALL_DEV_DEPS" ] ; then poetry install --only main --no-interaction ; else poetry install --no-interaction ; fi


COPY . .
ENV PYTHONPATH=.
ENV PATH="/app/.venv/bin:$PATH"

CMD ["hypercorn", "--config=hypercorn.toml", "quart_demo/asgi:app"]

EXPOSE 8080
