import logging
import os


def setup_logger(project_name: str, logger_folderpath: str = "logs") -> logging.Logger:
    """
    Creates a logger for that project name and creates the filehandler with
    the corresponding file
    """

    logging.basicConfig(level=logging.INFO)
    logger: logging.Logger = logging.getLogger(project_name)

    os.makedirs("logs", exist_ok=True)

    logger_filepath: str = os.path.join(logger_folderpath, f"{project_name}.log")

    file_handler = logging.FileHandler(logger_filepath)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    # Only annotate new run if its not the first iteration for that log file
    if os.path.getsize(logger_filepath) > 0:
        with open(logger_filepath, "a") as file:
            file.write("\nStarting a new run.\n\n")

    return logger
