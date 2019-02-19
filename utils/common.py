import os
import errno


def create_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return directory


def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data
