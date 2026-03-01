import logging
import datetime as dt
from dateutil.relativedelta import relativedelta
from typing import List, Any, Generator, Tuple


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


def chunk_list_equal_size(objects: List[Any], batch_size: int) -> List[List[Any]]:
    """ Returns a list of objects divided into chunks of size 'batch_size' """
    result = list([])
    for i in range(0, len(objects), batch_size):
        result.append(objects[i:i + batch_size])
    return result


def chunk_list_n_elements(elements: List[Any], number: int) -> List[List[Any]]:
    """ Returns a list of objects divided into 'number' chunks """
    result = list([])
    for i in range(0, number):
        result.append(elements[i::number])
    return result


def date_range(start_date: dt.datetime, end_date: dt.datetime | None = None, interval: str = "d") -> Generator[Tuple[dt.datetime, dt.datetime], None, None]:
    if end_date is None:
        end_date = dt.datetime.now()

    if interval == "h":
        sd = start_date.replace(minute=0, second=0)
        ed = end_date.replace(minute=0, second=0)
        for i in range(int((ed - sd).total_seconds()//3600) + 1):
            date = sd + dt.timedelta(hours=i)
            yield date, sd + dt.timedelta(hours=i+1)
    elif interval == "d":
        sd = start_date.replace(hour=0, minute=0, second=0)
        ed = end_date.replace(hour=0, minute=0, second=0)
        for i in range((ed - sd).days + 1):
            date = sd + dt.timedelta(days=i)
            yield date, sd + dt.timedelta(days=i+1)
    elif interval == "m":
        sd = start_date.replace(day=1, hour=0, minute=0, second=0)
        ed = end_date.replace(day=1, hour=0, minute=0, second=0)
        for i in range((ed.year - sd.year) * 12 + (ed.month - sd.month) + 1):
            date = sd + relativedelta(months=i)
            yield date, sd + relativedelta(months=i+1)
    elif interval == "y":
        sd = start_date.replace(month=1, day=1, hour=0, minute=0, second=0)
        ed = end_date.replace(month=1, day=1, hour=0, minute=0, second=0)
        for i in range(ed.year - sd.year + 1):
            date = sd + relativedelta(years=i)
            yield date, sd + relativedelta(years=i+1)
    else:
        raise ValueError(f"Unknown interval '{interval}'. Should be 'h', 'd', 'm' or 'y'.")

