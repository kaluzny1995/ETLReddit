class NoNewFileError(Exception):
    """ Raised when no new file is available for ingestion """
    pass

class JsonFileNotFoundError(Exception):
    """ Raised when a JSON file is not found """
    pass
