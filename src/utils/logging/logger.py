from logging import config

from .config import get_logging_config


def init_logger(name: str = "", is_debug: bool = False) -> None:
    """
    Initializes the logger with the specified configuration.

    This function sets up logging for the application by generating a logging configuration
    using `get_logging_config` and applying it through Python's `logging.config.dictConfig`.

    Args:
        name (str): The name of the logger. Defaults to an empty string,
                    which applies the configuration to the root logger.
        is_debug (bool): Flag to indicate whether the application is in debug mode.
                        If True, detailed logging with the `DEBUG` level is enabled. Defaults to False.

    Returns:
        None

    Usage:
        init_logger(name="my_app", is_debug=True)
    """
    cfg = get_logging_config(name=name, is_debug=is_debug)
    config.dictConfig(cfg)
