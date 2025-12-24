import logging
import os
import sys
from datetime import datetime

# ================= CONFIG =================
WRITE_LOGS = True
WRITE_TO_TERMINAL = True
LOG_FILENAME = "backup.log"
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
        file_handler = logging.FileHandler(
            log_path,
            mode="w",  # 🔥 overwrite every run
            encoding="utf-8"
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
    if WRITE_LOGS or WRITE_TO_TERMINAL:
        logging.info(text)


def error(text):
    if WRITE_LOGS or WRITE_TO_TERMINAL:
        logging.error(text)


