from . import *

""""""

import logging

from . import settings

# Suppresses warnings from pywavefront when importing incompletely imported OBJ files
logging.getLogger("pywavefront").setLevel(logging.ERROR)


def setup(logger_name: str, logger_folderpath: str = settings.Folders.LOGS) -> Logger:
    """
    Creates a logger for that project name and creates the filehandler with
    the corresponding file
    """

    logging.basicConfig(level=settings.Logging.LEVEL)
    logger: Logger = logging.getLogger(logger_name)

    os.makedirs("logs", exist_ok=True)

    logger_filepath: str = os.path.join(logger_folderpath, f"{logger_name}.log")

    file_handler = logging.FileHandler(logger_filepath)
    file_handler.setLevel(settings.Logging.LEVEL_FILE)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    # Only annotate new run if its not the first iteration for that log file
    if os.path.getsize(logger_filepath) > 0:
        with open(logger_filepath, "a") as file:
            file.write("\nStarting a new run.\n\n")

    return logger


def cleanup(logger: Optional[Logger]) -> None:
    if logger is not None:
        handlers: list[logging.Handler] = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        logging.getLogger().handlers.clear()
