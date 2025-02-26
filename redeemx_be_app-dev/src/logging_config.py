import logging
import logging.config
import os


LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "app.log"),
            "formatter": "detailed"
        },
        "error_file": {  
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "formatter": "detailed"
        }
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console", "file", "error_file"], 
            "propagate": False
        },
        "fastapi": {
            "level": "DEBUG",
            "handlers": ["console", "file", "error_file"],
            "propagate": False
        },
        "app": {  
            "level": "DEBUG",
            "handlers": ["console", "file", "error_file"],
            "propagate": False
        }
    }
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Get logger for application
logger = logging.getLogger("app")
