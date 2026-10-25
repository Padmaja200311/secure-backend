import logging
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        file_handler = logging.FileHandler(
            "logs/app.log",
            mode="a",
            encoding="utf-8"
        )

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)