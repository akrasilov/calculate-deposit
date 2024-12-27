_NOISY_LOGGERS = [
    "uvicorn",
    "uvicorn.access",
    "uvicorn.error",
    "uvicorn.asgi",
    "httpx",
]


def get_logging_config(name: str = "", is_debug: bool = False) -> dict:
    """
    Generates a logging configuration for the application.

    The function provides a structured dictionary compatible with Python's logging configuration.
    It supports both JSON and default text-based logging formats, and adjusts log levels for noisy loggers.

    Args:
        name (str): The name of the main logger. Defaults to an empty string.
        is_debug (bool): Flag to indicate whether the application is in debug mode.
                         If True, more detailed logging is enabled. Defaults to False.

    Returns:
        dict: A dictionary containing the logging configuration, including formatters, handlers, and loggers.

    Usage:
        config = get_logging_config(name="my_app", is_debug=True)
        logging.config.dictConfig(config)
    """
    handlers = ["default"] if is_debug else ["json"]
    noisy_loggers_level = "INFO" if is_debug else "ERROR"
    level = "DEBUG" if is_debug else "INFO"

    noisy_loggers_conf = {
        name: {
            "handlers": handlers,
            "level": noisy_loggers_level,
            "propagate": False,
        }
        for name in _NOISY_LOGGERS
    }
    message_fromat = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": message_fromat,
            },
            "default": {"format": message_fromat},
        },
        "handlers": {
            "json": {
                "formatter": "json",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            name: {
                "handlers": handlers,
                "level": level,
                "propagate": False,
            },
            **noisy_loggers_conf,
        },
    }
