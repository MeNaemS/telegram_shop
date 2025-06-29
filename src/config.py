from dynaconf import Dynaconf
from pathlib import Path
from adaptix import Retort
from src.config_schema import Config

BASE_PATH = Path(__file__).resolve().parent.parent
retort: Retort = Retort()
config: Config = retort.load(
    Dynaconf(
        settings_files=[
            BASE_PATH / "configs" / "config.toml",
            BASE_PATH / "configs" / "secret.toml"
        ],
        environments=True,
        merge_enabled=True,
        load_dotenv=True
    ),
    Config
)
