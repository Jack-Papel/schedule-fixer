"""
fs_util, not to be confused with fsutil
A utility class defining useful functions for working with files.

:author Jack Papel
"""
from os import path  # TODO switch to pathlib.Path, maybe


# TODO Verify this works on all systems
def fixed_path(save_dir: str, original_filepath: str) -> str:
    """
    Get the path of the fixed file.
    :param save_dir: The directory to save the file in
    :param original_filepath: The path of the original file
    :return: The new path of the fixed file
    """
    if save_dir is None:
        return path.splitext(original_filepath)[0] + '_fixed' + path.splitext(original_filepath)[1]
    return path.join(save_dir, path.splitext(path.basename(original_filepath))[0] +
                     "_fixed" + path.splitext(original_filepath)[1])


def get_dir(filepath: str) -> str:
    """
    Get the directory of the given file.
    :param filepath: The path to the file
    :return: The directory of the file
    """
    return path.dirname(filepath)


def name_and_extension(filepath: str) -> str:
    """
    Return the last part of the path: The file name and extension.
    :param filepath: The full path to the file
    :return: The file name and extension
    """
    name, ext = path.splitext(path.basename(filepath))
    return name + ext
