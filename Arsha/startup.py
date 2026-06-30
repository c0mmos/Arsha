import os
import logging
from pathlib import Path

from django.core.management import call_command
from filelock import FileLock, Timeout

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

LOCK_FILE = BASE_DIR / ".startup.lock"
DONE_FILE = BASE_DIR / ".startup.done"


def run_startup_tasks():
    """
    Run migrate and collectstatic once when the application starts.
    Safe for multiple Gunicorn workers.
    """

    try:
        with FileLock(str(LOCK_FILE), timeout=30):

            # Another worker already finished.
            if DONE_FILE.exists():
                logger.info("Startup tasks already completed.")
                return

            logger.info("Running migrations...")
            call_command("migrate", interactive=False)

            logger.info("Running collectstatic...")
            call_command("collectstatic", interactive=False, verbosity=1)

            DONE_FILE.touch()

            logger.info("Startup tasks finished.")

    except Timeout:
        logger.info("Another worker is performing startup tasks.")