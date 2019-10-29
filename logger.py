import logging

def get_logger(namespace):
    """Creates a console logger

    Args:
        namespace (str): Namespace for this logger

    Returns:
        obj: Logging object
    """
    namespace = __name__ if not namespace else namespace

    # create logger with namespace
    logger = logging.getLogger(namespace)
    logger.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
