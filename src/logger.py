import logging
from colorama import init, Fore, Style

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }
    def format(self, record):
        color = self.COLORS.get(record.levelno, '')
        message = super().format(record)
        return color + message + Style.RESET_ALL

@staticmethod
def initialize_logger(level=logging.INFO):
    """
    Set up logging configuration.
    Args:
        level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
    """
    log_format = '%(asctime)s - %(name)s - [%(levelname)s]: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler()
        ]
    )
    # Apply color formatting to the root logger's console handler
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(ColorFormatter(log_format, datefmt=date_format))
    # Add file handler
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logging.getLogger().addHandler(file_handler)