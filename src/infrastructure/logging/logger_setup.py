from logging import Logger, config as logging_config, getLogger
import sys
from src.config import config
from src.infrastructure.logging.logger_config_schema import LoggerConfigSchema


def setup_logger() -> Logger:
    log_level: str = config.log_level.upper()
    log_file: str = "/app/logs/telegram.log" if not config.debug else "telegram.log"
    log_config: LoggerConfigSchema = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
                "stream": sys.stderr,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_file,
                "maxBytes": 5_000_000,
                "backupCount": 3,
                "formatter": "default",
                "level": log_level,
            },
        },
        "root": {
            "handlers": ["file"],
            "level": log_level,
        },
        "loggers": {
            "src": {
                "level": log_level,
                "handlers": ["file"],
                "propagate": False,
            },
            "config": {
                "level": log_level,
                "handlers": ["file"],
                "propagate": False,
            }
        },
    }
    logging_config.dictConfig(log_config)
    logger = getLogger("src.infrastructure.logging")
    logger.info("Logging system initialized")
    return logger