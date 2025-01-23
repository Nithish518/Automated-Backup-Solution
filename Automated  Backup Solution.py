import os
import subprocess
import logging
from datetime import datetime

# Configuration
SOURCE_DIRECTORY = "/path/to/source/directory"
REMOTE_SERVER = "user@remote-server-address"
REMOTE_DIRECTORY = "/path/to/remote/directory"
LOG_FILE = "backup.log"

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_and_print(message, level="info"):
    """Log a message to both the console and log file."""
    print(message)
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

def perform_backup():
    """Performs the backup using rsync."""
    try:
        log_and_print("Starting backup operation...")

        # Ensure the source directory exists
        if not os.path.exists(SOURCE_DIRECTORY):
            raise FileNotFoundError(f"Source directory does not exist: {SOURCE_DIRECTORY}")

        # Build the rsync command
        rsync_command = [
            "rsync",
            "-avz",  # Archive mode, verbose, compress
            SOURCE_DIRECTORY,
            f"{REMOTE_SERVER}:{REMOTE_DIRECTORY}"
        ]

        # Execute the command
        result = subprocess.run(rsync_command, capture_output=True, text=True)

        if result.returncode == 0:
            log_and_print("Backup completed successfully.")
            log_and_print(result.stdout)
        else:
            log_and_print("Backup failed.", level="error")
            log_and_print(result.stderr, level="error")
    except Exception as e:
        log_and_print(f"Backup operation failed with exception: {e}", level="error")

def generate_backup_report():
    """Generate a backup report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_and_print("Generating backup report...")
    try:
        with open(LOG_FILE, "r") as log:
            lines = log.readlines()

        report_file = f"backup_report_{now.replace(':', '_').replace(' ', '_')}.txt"
        with open(report_file, "w") as report:
            report.write(f"Backup Report - {now}\n")
            report.write("================================\n")
            report.writelines(lines[-50:])  # Include the last 50 log lines for context

        log_and_print(f"Backup report generated: {report_file}")
    except Exception as e:
        log_and_print(f"Failed to generate backup report: {e}", level="error")

if __name__ == "__main__":
    perform_backup()
    generate_backup_report()
