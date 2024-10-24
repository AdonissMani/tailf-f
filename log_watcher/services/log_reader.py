import os

def get_last_lines(file_path, num_lines=10):
    """
    Returns the last N lines of a given file.
    """
    with open(file_path, "rb") as f:
        # Seek to the end of the file
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        buffer_size = 1024
        data = []
        while file_size > 0 and len(data) < num_lines:
            # Read a chunk of data from the file, seeking backwards from the end
            if file_size < buffer_size:
                buffer_size = file_size
            f.seek(-buffer_size, os.SEEK_END)
            block_data = f.read(buffer_size).decode('utf-8').splitlines()
            data = block_data + data
            file_size -= buffer_size
        # Return the last N lines
        return "\n".join(data[-num_lines:])
