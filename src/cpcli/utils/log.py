import logging


def initialize_logger():
    # Create directory to save all logs data
    # Setup logging config
    logging.basicConfig(
        level=logging.DEBUG,
        format=u'[#] %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
    )
