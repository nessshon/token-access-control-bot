import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_level=logging.INFO, logs_dir=".logs") -> None:
    """
    Set up logging configuration.

    Args:
        log_level (int): Logging level (default is INFO).
        logs_dir (str): Directory for log files (default is ".logs").
    """
    # Ensure the logs directory exists
    os.makedirs(logs_dir, exist_ok=True)

    # Set up basic logging configuration for the root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
        handlers=[
            TimedRotatingFileHandler(
                filename=os.path.join(logs_dir, f"bot.log"),
                when="D",
                interval=1,
                backupCount=31,
            ),
            logging.StreamHandler(),
        ]
    )

    # Set the log level for specific loggers
    _set_logger_level("httpx", logging.CRITICAL)
    _set_logger_level("aiogram.event", logging.CRITICAL)
    _set_logger_level("apscheduler.scheduler", logging.CRITICAL)
    _set_logger_level("apscheduler.executors.default", logging.CRITICAL)


def _set_logger_level(logger_name: str, level: int) -> None:
    """
    Set the log level for a specific logger.

    Args:
        logger_name (str): Name of the logger.
        level (int): Logging level.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
