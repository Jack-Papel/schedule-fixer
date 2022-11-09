# fs_util, not to be confused with fsutil
from os import path


# Verify this works on all systems
def copy_path(filepath: str) -> str:
    return path.join(path.dirname(filepath), path.splitext(path.basename(filepath))[0] +
                     "_copy" + path.splitext(filepath)[1])


def name_and_extension(filepath: str) -> str:
    name, ext = path.splitext(path.basename(filepath))
    return name + ext
