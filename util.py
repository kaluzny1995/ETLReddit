import logging
from typing import List, Any


def setup_logger(name, log_file, level=logging.INFO):
    """ Setup logger """

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def get_start_date_string_from_filename(filename: str) -> str:
    """ Returns the first datetime object from a filename\n
        Example: 'reddits_corgi_2026-01-01T00:00:00_2027-01-01T00:00:00.json'\n
        Should return: 2026-01-01T00:00:00 """
    return filename.split("_")[-2]


def get_end_date_string_from_filename(filename: str) -> str:
    """ Returns the second datetime object from a filename\n
        Example: 'reddits_corgi_2026-01-01T00:00:00_2027-01-01T00:00:00.json'\n
        Should return: 2027-01-01T00:00:00 """
    return filename.split("_")[-1].split(".")[0]


def chunk_list(objects: List[Any], batch_size: int) -> List[List[Any]]:
    """ Returns a list of objects divided into chunks of size batch_size """
    result = list([])
    for i in range(0, len(objects), batch_size):
        result.append(objects[i:i + batch_size])
    return result
