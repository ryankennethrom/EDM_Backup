import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

# ================= CONFIG =================
WRITE_LOGS = True
WRITE_TO_TERMINAL = True
LOG_FILENAME = "backup.log"
DAYS_TO_KEEP = 7
# =========================================


def setup_logging():
    # Detect running as EXE or script
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, LOG_FILENAME)

    handlers = []

    if WRITE_LOGS:
        file_handler = TimedRotatingFileHandler(
            log_path,
            when="midnight",      # rotate daily
            interval=1,
            backupCount=DAYS_TO_KEEP,  # 🔥 keep last 7 logs
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

    logging.info("========== PROGRAM START ==========")

setup_logging()

def info(text):
    logging.info(text)


def error(text):
    logging.error(text)
