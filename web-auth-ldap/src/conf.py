import logging


def set_log_level(log_level="INFO"):
    log_format = '%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] %(message)s'

    logging.basicConfig(
        datefmt='%Y-%m-%dT%H:%M:%S%z',
        format=log_format,
        level=log_level
    )
