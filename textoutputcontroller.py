import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from colorama import Fore, Style, init

# ================= CONFIG =================
WRITE_LOGS = True
WRITE_TO_TERMINAL = True
DAYS_TO_KEEP = 7
LOG_FILENAME = "backup.log"
# =========================================

# Initialize colorama for Windows
init(autoreset=True)

def setup_logging():
    # Detect running as EXE or script
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(base_dir, "backup_logs")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, LOG_FILENAME)

    handlers = []

    if WRITE_LOGS:
        file_handler = TimedRotatingFileHandler(
            log_path,
            when="midnight",
            interval=1,
            backupCount=DAYS_TO_KEEP,
            encoding="utf-8",
            utc=False
        )
        file_handler.setLevel(logging.INFO)
        handlers.append(file_handler)

    if WRITE_TO_TERMINAL:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers
    )


setup_logging()

# ================= API =================
def info(text):
    logging.info(text)


def error(text):
    logging.error(text)


def warn(text):
    """
    Print a big, eye-catching warning.
    Colors the message yellow in the terminal and logs it normally.
    """
    logging.warning(text)  # log normally

    # Build terminal message
    border = "*" * 80
    warning_title = Fore.YELLOW + Style.BRIGHT + "!!! WARNING !!!" + Style.RESET_ALL
    message = f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    out = ("\n" + border + "\n")
    out += (warning_title + "\n")
    out += (("-" * len(border)) + "\n")
    out += (message + "\n")
    out += (border + "\n")

    logging.info(text)


