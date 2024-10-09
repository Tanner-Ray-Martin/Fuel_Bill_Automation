"""
file_finder.py

A module to find the most recently modified file in a directory that matches given criteria.
"""

import os
import re
from datetime import datetime, timedelta


def find_latest_file(
    folder_path,
    extension=None,
    filename_pattern=None,
    size_limit=None,
    modified_within=None,
):
    """
    Find the latest modified file in the specified folder that matches given criteria.

    :param folder_path: The path to the folder to search.
    :param extension: (Optional) File extension to filter by (e.g., '.txt').
    :param filename_pattern: (Optional) A regex pattern that filenames should match.
    :param size_limit: (Optional) A tuple (min_size, max_size) in bytes.
                      Use None for min_size or max_size if you don't want to set a limit.
    :param modified_within: (Optional) A timedelta object representing the time window from now.
                            Only files modified within this time window are considered.
    :return: The path to the latest modified file, or None if no files match.
    """
    latest_file = None
    latest_mtime = None
    now = datetime.now()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Filter by extension
            if extension and not file.lower().endswith(extension.lower()):
                continue

            # Filter by filename pattern
            if filename_pattern and not re.search(filename_pattern, file):
                continue

            file_path = os.path.join(root, file)
            try:
                stat = os.stat(file_path)
            except FileNotFoundError:
                # The file might have been removed between os.walk and os.stat
                continue

            mtime = datetime.fromtimestamp(stat.st_mtime)
            size = stat.st_size

            # Filter by size
            if size_limit:
                min_size, max_size = size_limit
                if min_size is not None and size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue

            # Filter by modified time
            if modified_within:
                if now - mtime > modified_within:
                    continue

            # Update the latest file found
            if latest_mtime is None or mtime > latest_mtime:
                latest_file = file_path
                latest_mtime = mtime

    return latest_file
