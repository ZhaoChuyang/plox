import os


def check_path_exists(path: str):
    """
    Return true if the given path exists, false if not.
    """
    return os.path.exists(path)
