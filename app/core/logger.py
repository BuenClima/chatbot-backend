import logging
import logging.config

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",  # Set the console handler to capture DEBUG and above
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",  # Set the root logger level to DEBUG
            "propagate": False,
        }
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)
