"""
FileUilts.py

Utilities related to files.

"""
import json
import os


def relative_path(path: str) -> str:
    """
    Returns the absolute path of a file based on relative path input.
    "Relative" means relative to this script.
    :param path: relative path.
    :return: absolute path, assuming relative path is based on this script.
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path)
    return filename


def write_obj(path: str, obj: object) -> bool:
    """
    Save an object (using json dump) to a specific path, relative to this utility script.
    :param path: relative path.
    :param obj: object to save.
    :return: whether operation is successful.
    """
    try:
        with open(relative_path(path), 'w') as f:
            json.dump(obj, f)
        return True
    except Exception as e:
        print("Failed to save file: %s" % str(e))
        return False
