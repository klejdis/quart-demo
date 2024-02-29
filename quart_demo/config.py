import typed_settings as typed_settings


@typed_settings.settings
class Quart:
    DEBUG: bool
    ENV: str
    TESTING: bool


@typed_settings.settings
class Database:
    uri: str
    echo: bool


@typed_settings.settings
class JsonPlaceholder:
    server_url: str


@typed_settings.settings
class Settings:
    quart: Quart
    base_path: str
    database: Database
    json_placeholder: JsonPlaceholder


settings = typed_settings.load_settings(
    cls=Settings,
    loaders=[
        typed_settings.FileLoader(
            files=[typed_settings.find("config/config.toml")],
            env_var="CONFIG",
            formats={
                "*.toml": typed_settings.TomlFormat("quart_demo"),
            },
        ),
        typed_settings.EnvLoader(prefix=""),
    ],
)
