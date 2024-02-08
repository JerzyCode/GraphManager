import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

LOG_COLORS = {
    logging.DEBUG: GREEN,
    logging.INFO: WHITE,
    logging.WARNING: YELLOW,
    logging.ERROR: RED,
    logging.CRITICAL: MAGENTA, }


def create_color_format(color_code):
    return f"\033[1;3{color_code}m%(asctime)s - %(name)s - %(levelname)s - %(message)s\033[0m"


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color_code = LOG_COLORS.get(record.levelno, WHITE)
        formatter = logging.Formatter(create_color_format(color_code))
        return formatter.format(record)


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    return logger
