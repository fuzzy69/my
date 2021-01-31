from os import listdir, makedirs, remove
from os.path import exists, isfile, join
from typing import AnyStr, Iterable, List, Optional, Union

try:
    from libs.my.core.text.utilities import get_match
except ModuleNotFoundError:
    from core.text.utilities import get_match


def ensure_dir(dir_path: AnyStr) -> Union[bool, AnyStr]:
    """
    Create directory path if it doesn't exists
    :param str dir_path: full path to target directory
    :return: return True if directory path is created or False if it already exists
    :raise: when creating directories fails (permission issue, unreachable target media, etc ...)
    """
    if not exists(dir_path):
        try:
            makedirs(dir_path)
        except Exception as e:
            return str(e)

    return True


def clear_dir(dir_path: str, filter_text: Optional[AnyStr]) -> List[AnyStr]:
    """
    Removes files from a directory
    :param str dir_path: path to a directory with files to remove
    :return: list of removed file paths
    """
    removed_files = []
    for file_path in list_dir(dir_path):
        if filter_text is not None:
            # match = get_match(filter_regex, file_path)
            # matches = match(filter_regex, file_path)
            # if not matches:
            if filter_text not in file_path:
                continue
        if isfile(file_path):
            remove(file_path)
            removed_files.append(file_path)

    return removed_files


def list_dir(dir_path: AnyStr, full_path: bool = True) -> Iterable[AnyStr]:
    """Yields file names or full file paths in chosen directory"""
    for file_ in listdir(dir_path):
        if full_path:
            file_path = join(dir_path, file_)
            yield file_path
        else:
            yield file_
