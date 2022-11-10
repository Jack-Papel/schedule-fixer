"""
fs_util, not to be confused with fsutil
A utility class defining useful functions for working with files.

:author Jack Papel
"""
from os import path


# TODO Verify this works on all systems
def fixed_path(filepath: str) -> str:
    """
    Get the path of the fixed file.
    :param filepath: The path of the original file
    :return: The new path of the fixed file
    """
    return path.join(path.dirname(filepath), path.splitext(path.basename(filepath))[0] +
                     "_fixed" + path.splitext(filepath)[1])


def name_and_extension(filepath: str) -> str:
    """
    Return the last part of the path: The file name and extension.
    :param filepath: The full path to the file
    :return: The file name and extension
    """
    name, ext = path.splitext(path.basename(filepath))
    return name + ext
