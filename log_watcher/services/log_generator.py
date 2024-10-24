import time
from datetime import datetime
log_file_path = "sample.log"

def append_log() -> None:
    """
    Appends 10 log entries to the log file specified by log_file_path.
    
    """
    with open(log_file_path, "a") as f:
        for i in range(10):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Log entry : {current_time} - {i}\n"
            f.write(log_message)
        # Add an extra newline at the end of the file
        f.write("\n")

if __name__ == "__main__":
    while True:
        append_log()
        print("new log generated")
        time.sleep(5)