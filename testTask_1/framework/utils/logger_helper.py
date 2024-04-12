import sys
from typing import Any
from loguru import logger


class Logger:
    __logger = logger
    __logger.remove()
    __logger.add(sys.stderr, format="<blue>[{level}]</blue> : <green>{message}</green>", colorize=True)

    @staticmethod
    def info(message: str) -> None:
        Logger.__logger.info(message)

    @staticmethod
    def debug(message: str) -> None:
        Logger.__logger.debug(message)

    @staticmethod
    def warning(message: str) -> None:
        Logger.__logger.warning(message)

    @staticmethod
    def error(message: str) -> None:
        Logger.__logger.error(message)

    @staticmethod
    def step(message: str) -> Any:
        def step_decorator(step_method: Any) -> Any:
            Logger.__logger.info(f'STEP: {message}')
            return step_method

        return step_decorator

